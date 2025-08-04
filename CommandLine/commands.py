import sys
from datetime import datetime

class Command:
    def __init__(self, app, timestamp=None):
        self.app = app
        self.timestamp = timestamp or datetime.now().isoformat()

    def execute(self): raise NotImplementedError
    def undo(self): raise NotImplementedError
    def to_dict(self): return {'type': self.__class__.__name__, 'timestamp': self.timestamp, 'data': self._get_data_for_serialization()}
    def _get_data_for_serialization(self): raise NotImplementedError

    def get_description(self):
        try:
            dt_obj = datetime.fromisoformat(self.timestamp)
            time_str = dt_obj.strftime("%m/%d %H:%M:%S")
            return f"{self.__class__.__name__} ({time_str})"
        except (ValueError, TypeError):
            return f"{self.__class__.__name__} (Timestamp: {self.timestamp})"

    @classmethod
    def from_dict(cls, app, data_dict):
        command_type_name = data_dict['type']
        command_class = getattr(sys.modules[__name__], command_type_name, None)
        if command_class and issubclass(command_class, Command):
            try:
                return command_class._from_serializable_data(app, data_dict['data'], data_dict['timestamp'])
            except KeyError as e:
                print(f"Warning: Missing key '{e}' in data for command type '{command_type_name}'. Skipping command.")
                return None
        print(f"Warning: Unknown command type '{command_type_name}' in undo/redo history.")
        return None

    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): raise NotImplementedError

class AddItemCommand(Command):
    def __init__(self, app, item_id, item_type, item_data, old_next_id_num, timestamp=None):
        super().__init__(app, timestamp)
        self.item_id = item_id
        self.item_type = item_type
        self.item_data = item_data
        self.old_next_id_num = old_next_id_num

    def execute(self):
        if self.item_type == 'student':
            data_source = self.app.classroom.students
            data_source[self.item_id] = self.item_data.copy()
            self.app.classroom.settings["next_student_id_num"] = self.item_data.get('original_next_id_num_after_add', self.app.classroom.settings["next_student_id_num"])
        else: # furniture
            data_source = self.app.classroom.furniture
            data_source[self.item_id] = self.item_data.copy()
            self.app.classroom.settings["next_furniture_id_num"] = self.item_data.get('original_next_id_num_after_add', self.app.classroom.settings["next_furniture_id_num"])

        self.app.update_all_tables()

    def undo(self):
        if self.item_type == 'student':
            data_source = self.app.classroom.students
            if self.item_id in data_source:
                del data_source[self.item_id]
            self.app.classroom.settings["next_student_id_num"] = self.old_next_id_num
        else: # furniture
            data_source = self.app.classroom.furniture
            if self.item_id in data_source:
                del data_source[self.item_id]
            self.app.classroom.settings["next_furniture_id_num"] = self.old_next_id_num

        self.app.update_all_tables()

    def _get_data_for_serialization(self): return {'item_id': self.item_id, 'item_type': self.item_type, 'item_data': self.item_data, 'old_next_id_num': self.old_next_id_num}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['item_id'], data['item_type'], data['item_data'], data['old_next_id_num'], timestamp)

class DeleteItemCommand(Command):
    def __init__(self, app, item_id, item_type, item_data, associated_logs=None, associated_homework_logs=None, timestamp=None):
        super().__init__(app, timestamp)
        self.item_id = item_id
        self.item_type = item_type
        self.item_data = item_data
        self.associated_logs = associated_logs or []
        self.associated_homework_logs = associated_homework_logs or []

    def execute(self):
        if self.item_type == 'student':
            if self.item_id in self.app.classroom.students:
                del self.app.classroom.students[self.item_id]
            self.app.classroom.behavior_log = [log for log in self.app.classroom.behavior_log if log["student_id"] != self.item_id]
            self.app.classroom.homework_log = [log for log in self.app.classroom.homework_log if log["student_id"] != self.item_id]
        else: # furniture
            if self.item_id in self.app.classroom.furniture:
                del self.app.classroom.furniture[self.item_id]

        self.app.update_all_tables()

    def undo(self):
        if self.item_type == 'student':
            self.app.classroom.students[self.item_id] = self.item_data.copy()
            for log_entry in self.associated_logs:
                if log_entry not in self.app.classroom.behavior_log: self.app.classroom.behavior_log.append(log_entry.copy())
            self.app.classroom.behavior_log.sort(key=lambda x: x.get("timestamp", ""))
            for hw_log_entry in self.associated_homework_logs:
                if hw_log_entry not in self.app.classroom.homework_log: self.app.classroom.homework_log.append(hw_log_entry.copy())
            self.app.classroom.homework_log.sort(key=lambda x: x.get("timestamp", ""))
        else: # furniture
            self.app.classroom.furniture[self.item_id] = self.item_data.copy()

        self.app.update_all_tables()

    def _get_data_for_serialization(self):
        return {'item_id': self.item_id, 'item_type': self.item_type, 'item_data': self.item_data, 'associated_logs': self.associated_logs, 'associated_homework_logs': self.associated_homework_logs}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        return cls(app, data['item_id'], data['item_type'], data['item_data'], data.get('associated_logs'), data.get('associated_homework_logs'), timestamp)

class EditItemCommand(Command):
    def __init__(self, app, item_id, item_type, old_item_data, new_item_data_changes, timestamp=None):
        super().__init__(app, timestamp)
        self.item_id = item_id
        self.item_type = item_type
        self.old_item_data_snapshot = old_item_data
        self.new_item_data_changes = new_item_data_changes

    def execute(self):
        data_source = self.app.classroom.students if self.item_type == 'student' else self.app.classroom.furniture
        if self.item_id in data_source:
            data_source[self.item_id].update(self.new_item_data_changes)
        self.app.update_all_tables()

    def undo(self):
        data_source = self.app.classroom.students if self.item_type == 'student' else self.app.classroom.furniture
        if self.item_id in data_source:
            data_source[self.item_id] = self.old_item_data_snapshot.copy()
        self.app.update_all_tables()

    def _get_data_for_serialization(self):
        return {'item_id': self.item_id, 'item_type': self.item_type, 'old_item_data_snapshot': self.old_item_data_snapshot, 'new_item_data_changes': self.new_item_data_changes}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        return cls(app, data['item_id'], data['item_type'], data['old_item_data_snapshot'], data['new_item_data_changes'], timestamp)

class LogEntryCommand(Command):
    def __init__(self, app, log_entry, student_id, timestamp=None):
        super().__init__(app, timestamp)
        self.log_entry = log_entry
        self.student_id = student_id

    def execute(self):
        if not any(le == self.log_entry for le in self.app.classroom.behavior_log):
            self.app.classroom.behavior_log.append(self.log_entry.copy())
            self.app.classroom.behavior_log.sort(key=lambda x: x.get("timestamp", ""))
        self.app.update_all_tables()

    def undo(self):
        try:
            self.app.classroom.behavior_log.remove(self.log_entry)
        except ValueError:
            pass
        self.app.update_all_tables()

    def _get_data_for_serialization(self): return {'log_entry': self.log_entry, 'student_id': self.student_id}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['log_entry'], data['student_id'], timestamp)

class LogHomeworkEntryCommand(Command):
    def __init__(self, app, log_entry, student_id, timestamp=None):
        super().__init__(app, timestamp)
        self.log_entry = log_entry
        self.student_id = student_id

    def execute(self):
        if not any(le == self.log_entry for le in self.app.classroom.homework_log):
            self.app.classroom.homework_log.append(self.log_entry.copy())
            self.app.classroom.homework_log.sort(key=lambda x: x.get("timestamp", ""))
        self.app.update_all_tables()

    def undo(self):
        try:
            self.app.classroom.homework_log.remove(self.log_entry)
        except ValueError:
            pass
        self.app.update_all_tables()

    def _get_data_for_serialization(self): return {'log_entry': self.log_entry, 'student_id': self.student_id}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['log_entry'], data['student_id'], timestamp)
