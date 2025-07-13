package com.example.behaviorlogger.db.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "furniture_items")
data class FurnitureItemEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0L,
    val name: String?,
    val x: Float,
    val y: Float,
    val rotation: Float,
    val width: Float,
    val height: Float,
    val type: String,
    val color: String?,
    val isBehindStudents: Boolean
)
