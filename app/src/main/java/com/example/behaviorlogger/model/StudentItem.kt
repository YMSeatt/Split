package com.example.behaviorlogger.model

import java.time.LocalDate

data class StudentItem(
    val id: Long = 0L,
    val name: String,
    val studentId: String?,
    val x: Float,
    val y: Float,
    val rotation: Float,
    val width: Float,
    val height: Float,
    val isGroup: Boolean = false,
    val children: List<StudentItem>? = null,
    val lastBehavior: String?,
    val lastBehaviorTimestamp: String?,
    val lastQuiz: String?,
    val lastQuizTimestamp: String?,
    val lastHomework: String?,
    val lastHomeworkTimestamp: String?,
    val conditionalFormatting: List<ConditionalFormattingResult>? = null,
    val customFields: Map<String, String>? = null,
    val notes: String?,
    val dateOfBirth: LocalDate?,
    val contactInfo: String?
)

data class ConditionalFormattingResult(
    val ruleName: String,
    val formatting: Map<String, String>
)
