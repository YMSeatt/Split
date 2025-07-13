package com.example.behaviorlogger.model

import com.google.gson.annotations.SerializedName

// Main container for all settings
data class ClassroomSettings(
    @SerializedName("general")
    val general: GeneralSettings = GeneralSettings(),

    @SerializedName("student_box")
    val studentBox: StudentBoxSettings = StudentBoxSettings(),

    @SerializedName("behavior_quiz")
    val behaviorQuiz: BehaviorQuizSettings = BehaviorQuizSettings(),

    @SerializedName("homework")
    val homework: HomeworkSettings = HomeworkSettings(),

    @SerializedName("data_export")
    val dataExport: DataExportSettings = DataExportSettings(),

    @SerializedName("security")
    val security: SecuritySettings = SecuritySettings(),

    @SerializedName("custom_behaviors")
    val customBehaviors: List<String> = emptyList(),

    @SerializedName("custom_homework_statuses")
    val customHomeworkStatuses: List<String> = emptyList(),

    @SerializedName("custom_homework_types")
    val customHomeworkTypes: List<String> = emptyList(),

    @SerializedName("live_homework_select_options")
    val liveHomeworkSelectOptions: List<String> = emptyList(),

    @SerializedName("quiz_mark_types")
    val quizMarkTypes: List<MarkType> = emptyList(),

    @SerializedName("homework_mark_types")
    val homeworkMarkTypes: List<MarkType> = emptyList(),

    @SerializedName("quiz_templates")
    val quizTemplates: List<Template> = emptyList(),

    @SerializedName("homework_templates")
    val homeworkTemplates: List<Template> = emptyList(),

    @SerializedName("conditional_formatting_rules")
    val conditionalFormattingRules: List<ConditionalFormattingRule> = emptyList(),
)

// Sub-models for different settings categories
data class GeneralSettings(
    @SerializedName("show_names")
    val showNames: Boolean = true,
    @SerializedName("show_ids")
    val showIds: Boolean = false,
    @SerializedName("id_type")
    val idType: String = "Student ID",
    @SerializedName("language")
    val language: String = "English",
    @SerializedName("log_retention_days")
    val logRetentionDays: Int = 365,
    @SerializedName("theme")
    val theme: String = "System Default"
)

data class StudentBoxSettings(
    @SerializedName("show_last_behavior")
    val showLastBehavior: Boolean = true,
    @SerializedName("show_last_quiz")
    val showLastQuiz: Boolean = true,
    @SerializedName("show_last_homework")
    val showLastHomework: Boolean = true,
    @SerializedName("box_width")
    val boxWidth: Int = 100,
    @SerializedName("box_height")
    val boxHeight: Int = 60,
    @SerializedName("font_size")
    val fontSize: Int = 12,
    @SerializedName("corner_radius")
    val cornerRadius: Int = 8,
    @SerializedName("border_width")
    val borderWidth: Int = 1
)

data class BehaviorQuizSettings(
    @SerializedName("behavior_entry_mode")
    val behaviorEntryMode: String = "Menu",
    @SerializedName("quiz_entry_mode")
    val quizEntryMode: String = "Menu"
)

data class HomeworkSettings(
    @SerializedName("live_mode_default")
    val liveModeDefault: String = "Yes/No",
    @SerializedName("homework_entry_mode")
    val homeworkEntryMode: String = "Menu"
)

data class DataExportSettings(
    @SerializedName("csv_delimiter")
    val csvDelimiter: String = ",",
    @SerializedName("include_header")
    val includeHeader: Boolean = true,
    @SerializedName("default_export_format")
    val defaultExportFormat: String = "CSV"
)

data class SecuritySettings(
    @SerializedName("app_lock_enabled")
    val appLockEnabled: Boolean = false,
    @SerializedName("auto_lock_minutes")
    val autoLockMinutes: Int = 5,
    @SerializedName("app_password_hash")
    val appPasswordHash: String? = null
)

// Complex types used in settings
data class MarkType(
    @SerializedName("name")
    val name: String,
    @SerializedName("hotkey")
    val hotkey: String? = null,
    @SerializedName("color")
    val color: String? = null // Storing color as hex string e.g., "#FF0000"
)

data class Template(
    @SerializedName("name")
    val name: String,
    @SerializedName("items")
    val items: List<String>
)

data class ConditionalFormattingRule(
    @SerializedName("name")
    val name: String,
    @SerializedName("is_enabled")
    val isEnabled: Boolean = true,
    @SerializedName("priority")
    val priority: Int = 0,
    @SerializedName("condition")
    val condition: Condition,
    @SerializedName("formatting")
    val formatting: Formatting,
    @SerializedName("active_times")
    val activeTimes: List<ActiveTime>? = null,
    @SerializedName("active_modes")
    val activeModes: List<String>? = null // e.g., ["Behavior", "Quiz", "Homework"]
)

data class Condition(
    @SerializedName("type")
    val type: String, // e.g., "group", "behavior_count", "quiz_score_threshold"
    @SerializedName("parameters")
    val parameters: Map<String, String>
)

data class Formatting(
    @SerializedName("background_color")
    val backgroundColor: String? = null,
    @SerializedName("text_color")
    val textColor: String? = null,
    @SerializedName("border_color")
    val borderColor: String? = null,
    @SerializedName("icon")
    val icon: String? = null
)

data class ActiveTime(
    @SerializedName("day_of_week")
    val dayOfWeek: List<String>, // e.g., ["Monday", "Wednesday"]
    @SerializedName("start_time")
    val startTime: String, // "HH:mm"
    @SerializedName("end_time")
    val endTime: String // "HH:mm"
)
