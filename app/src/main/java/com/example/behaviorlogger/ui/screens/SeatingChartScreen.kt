package com.example.behaviorlogger.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.example.behaviorlogger.ui.viewmodel.SeatingChartViewModel

@Composable
fun SeatingChartScreen(viewModel: SeatingChartViewModel) {
    val students by viewModel.students.collectAsState()
    val settings by viewModel.settings.collectAsState()

    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        if (students.isEmpty()) {
            Text("No students found.")
        } else {
            Text("Seating Chart Screen with ${students.size} students.")
        }
    }
}
