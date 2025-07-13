package com.example.behaviorlogger.model

import java.time.LocalDateTime

data class HomeworkLog(
    val id: Long = 0L,
    val studentId: Long,
    val timestamp: LocalDateTime,
    val homeworkType: String,
    val status: String,
    val comment: String?
)
