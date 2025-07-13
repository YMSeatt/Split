package com.example.behaviorlogger.db.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.time.LocalDate

@Entity(tableName = "students")
data class StudentEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0L,
    val name: String,
    val studentId: String?,
    val x: Float,
    val y: Float,
    val rotation: Float,
    val width: Float,
    val height: Float,
    val isGroup: Boolean = false,
    // For groups, this will be a JSON string of child student IDs.
    // For individual students, it will be null.
    val childrenIds: String?,
    val notes: String?,
    val dateOfBirth: LocalDate?,
    val contactInfo: String?,
    // This will be a JSON string of custom fields
    val customFields: String?
)
