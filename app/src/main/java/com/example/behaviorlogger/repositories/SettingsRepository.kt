package com.example.behaviorlogger.repositories

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import com.example.behaviorlogger.model.ClassroomSettings
import com.google.gson.Gson
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

class SettingsRepository(private val context: Context) {

    private val gson = Gson()

    val classroomSettingsFlow: Flow<ClassroomSettings> = context.dataStore.data
        .map { preferences ->
            mapPreferencesToClassroomSettings(preferences)
        }

    private fun mapPreferencesToClassroomSettings(preferences: Preferences): ClassroomSettings {
        // This mapping function will be complex. For now, we'll just return a default
        // object. A full implementation would read each preference and construct the
        // ClassroomSettings object.
        return ClassroomSettings()
    }

    suspend fun updateSettings(settings: ClassroomSettings) {
        context.dataStore.edit { preferences ->
            // General
            preferences[AppSettingsKeys.SHOW_NAMES] = settings.general.showNames
            preferences[AppSettingsKeys.SHOW_IDS] = settings.general.showIds
            // ... and so on for all settings
        }
    }

    suspend fun updateAppPasswordHash(newHash: String?) {
        context.dataStore.edit { settings ->
            if (newHash == null) {
                settings.remove(AppSettingsKeys.APP_PASSWORD_HASH)
            } else {
                settings[AppSettingsKeys.APP_PASSWORD_HASH] = newHash
            }
        }
    }
}
