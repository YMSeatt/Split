package com.example.behaviorlogger.repositories

import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey

object AppSettingsKeys {
    // General
    val SHOW_NAMES = booleanPreferencesKey("show_names")
    val SHOW_IDS = booleanPreferencesKey("show_ids")
    val ID_TYPE = stringPreferencesKey("id_type")
    val LANGUAGE = stringPreferencesKey("language")
    val LOG_RETENTION_DAYS = intPreferencesKey("log_retention_days")
    val THEME = stringPreferencesKey("theme")

    // Student Box
    val SHOW_LAST_BEHAVIOR = booleanPreferencesKey("show_last_behavior")
    val SHOW_LAST_QUIZ = booleanPreferencesKey("show_last_quiz")
    val SHOW_LAST_HOMEWORK = booleanPreferencesKey("show_last_homework")
    val BOX_WIDTH = intPreferencesKey("box_width")
    val BOX_HEIGHT = intPreferencesKey("box_height")
    val FONT_SIZE = intPreferencesKey("font_size")
    val CORNER_RADIUS = intPreferencesKey("corner_radius")
    val BORDER_WIDTH = intPreferencesKey("border_width")

    // Behavior/Quiz
    val BEHAVIOR_ENTRY_MODE = stringPreferencesKey("behavior_entry_mode")
    val QUIZ_ENTRY_MODE = stringPreferencesKey("quiz_entry_mode")

    // Homework
    val LIVE_MODE_DEFAULT = stringPreferencesKey("live_mode_default")
    val HOMEWORK_ENTRY_MODE = stringPreferencesKey("homework_entry_mode")

    // Data Export
    val CSV_DELIMITER = stringPreferencesKey("csv_delimiter")
    val INCLUDE_HEADER = booleanPreferencesKey("include_header")
    val DEFAULT_EXPORT_FORMAT = stringPreferencesKey("default_export_format")

    // Security
    val APP_LOCK_ENABLED = booleanPreferencesKey("app_lock_enabled")
    val AUTO_LOCK_MINUTES = intPreferencesKey("auto_lock_minutes")
    val APP_PASSWORD_HASH = stringPreferencesKey("app_password_hash")

    // Complex lists (stored as JSON strings)
    val CUSTOM_BEHAVIORS = stringPreferencesKey("custom_behaviors")
    val CUSTOM_HOMEWORK_STATUSES = stringPreferencesKey("custom_homework_statuses")
    val CUSTOM_HOMEWORK_TYPES = stringPreferencesKey("custom_homework_types")
    val LIVE_HOMEWORK_SELECT_OPTIONS = stringPreferencesKey("live_homework_select_options")
    val QUIZ_MARK_TYPES = stringPreferencesKey("quiz_mark_types")
    val HOMEWORK_MARK_TYPES = stringPreferencesKey("homework_mark_types")
    val QUIZ_TEMPLATES = stringPreferencesKey("quiz_templates")
    val HOMEWORK_TEMPLATES = stringPreferencesKey("homework_templates")
    val CONDITIONAL_FORMATTING_RULES = stringPreferencesKey("conditional_formatting_rules")
}
