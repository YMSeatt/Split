package com.example.behaviorlogger.model

import java.time.LocalDateTime

data class QuizLog(
    val id: Long = 0L,
    val studentId: Long,
    val timestamp: LocalDateTime,
    val quizName: String,
    val score: String,
    val comment: String?
)
