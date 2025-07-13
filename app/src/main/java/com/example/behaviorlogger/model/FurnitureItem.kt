package com.example.behaviorlogger.model

data class FurnitureItem(
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
