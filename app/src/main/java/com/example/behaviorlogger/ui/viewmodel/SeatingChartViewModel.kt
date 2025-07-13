package com.example.behaviorlogger.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.behaviorlogger.model.StudentItem
import com.example.behaviorlogger.repositories.ClassroomRepository
import com.example.behaviorlogger.repositories.SettingsRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn

class SeatingChartViewModel(
    private val classroomRepository: ClassroomRepository,
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    val students: StateFlow<List<StudentItem>> = classroomRepository.students
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    val settings = settingsRepository.classroomSettingsFlow
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = com.example.behaviorlogger.model.ClassroomSettings()
        )
}
