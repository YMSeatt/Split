package com.example.behaviorlogger.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.behaviorlogger.ui.screens.SeatingChartScreen
import com.example.behaviorlogger.ui.viewmodel.SeatingChartViewModel

@Composable
fun AppNavigation(viewModel: SeatingChartViewModel) {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = AppRoutes.SEATING_CHART) {
        composable(AppRoutes.SEATING_CHART) {
            SeatingChartScreen(viewModel = viewModel)
        }
        // Add other composables here
    }
}
