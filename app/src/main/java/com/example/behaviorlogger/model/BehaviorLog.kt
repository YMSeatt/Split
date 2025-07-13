package com.example.behaviorlogger.model

import java.time.LocalDateTime

data class BehaviorLog(
    val id: Long = 0L,
    val studentId: Long,
    val timestamp: LocalDateTime,
    val behavior: String,
    val comment: String?
)
