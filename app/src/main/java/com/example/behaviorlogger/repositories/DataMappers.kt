package com.example.behaviorlogger.repositories

import com.example.behaviorlogger.db.entity.BehaviorLogEntity
import com.example.behaviorlogger.db.entity.FurnitureItemEntity
import com.example.behaviorlogger.db.entity.HomeworkLogEntity
import com.example.behaviorlogger.db.entity.QuizLogEntity
import com.example.behaviorlogger.db.entity.StudentEntity
import com.example.behaviorlogger.model.BehaviorLog
import com.example.behaviorlogger.model.FurnitureItem
import com.example.behaviorlogger.model.HomeworkLog
import com.example.behaviorlogger.model.QuizLog
import com.example.behaviorlogger.model.StudentItem
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

private val gson = Gson()

// Student Mappers
fun StudentEntity.toStudentItem(): StudentItem {
    val childrenList: List<StudentItem>? = if (isGroup && !childrenIds.isNullOrEmpty()) {
        // This is a simplified mapping. A real implementation would need to
        // fetch the actual StudentItem objects corresponding to the IDs.
        emptyList()
    } else {
        null
    }
    val customFieldsMap: Map<String, String>? = if (!customFields.isNullOrEmpty()) {
        gson.fromJson(customFields, object : TypeToken<Map<String, String>>() {}.type)
    } else {
        null
    }
    return StudentItem(
        id = id,
        name = name,
        studentId = studentId,
        x = x,
        y = y,
        rotation = rotation,
        width = width,
        height = height,
        isGroup = isGroup,
        children = childrenList,
        notes = notes,
        dateOfBirth = dateOfBirth,
        contactInfo = contactInfo,
        customFields = customFieldsMap,
        lastBehavior = null, // These will be populated by the repository
        lastBehaviorTimestamp = null,
        lastQuiz = null,
        lastQuizTimestamp = null,
        lastHomework = null,
        lastHomeworkTimestamp = null,
        conditionalFormatting = null
    )
}

fun StudentItem.toStudentEntity(): StudentEntity {
    val childrenIdsJson = if (isGroup && children != null) {
        gson.toJson(children.map { it.id })
    } else {
        null
    }
    val customFieldsJson = if (customFields != null) {
        gson.toJson(customFields)
    } else {
        null
    }
    return StudentEntity(
        id = id,
        name = name,
        studentId = studentId,
        x = x,
        y = y,
        rotation = rotation,
        width = width,
        height = height,
        isGroup = isGroup,
        childrenIds = childrenIdsJson,
        notes = notes,
        dateOfBirth = dateOfBirth,
        contactInfo = contactInfo,
        customFields = customFieldsJson
    )
}

// Furniture Mappers
fun FurnitureItemEntity.toFurnitureItem() = FurnitureItem(
    id = id,
    name = name,
    x = x,
    y = y,
    rotation = rotation,
    width = width,
    height = height,
    type = type,
    color = color,
    isBehindStudents = isBehindStudents
)

fun FurnitureItem.toFurnitureItemEntity() = FurnitureItemEntity(
    id = id,
    name = name,
    x = x,
    y = y,
    rotation = rotation,
    width = width,
    height = height,
    type = type,
    color = color,
    isBehindStudents = isBehindStudents
)

// Log Mappers
fun BehaviorLogEntity.toBehaviorLog() = BehaviorLog(
    id = id,
    studentId = studentId,
    timestamp = timestamp,
    behavior = behavior,
    comment = comment
)

fun BehaviorLog.toBehaviorLogEntity() = BehaviorLogEntity(
    id = id,
    studentId = studentId,
    timestamp = timestamp,
    behavior = behavior,
    comment = comment
)

fun QuizLogEntity.toQuizLog() = QuizLog(
    id = id,
    studentId = studentId,
    timestamp = timestamp,
    quizName = quizName,
    score = score,
    comment = comment
)

fun QuizLog.toQuizLogEntity() = QuizLogEntity(
    id = id,
    studentId = studentId,
    timestamp = timestamp,
    quizName = quizName,
    score = score,
    comment = comment
)

fun HomeworkLogEntity.toHomeworkLog() = HomeworkLog(
    id = id,
    studentId = studentId,
    timestamp = timestamp,
    homeworkType = homeworkType,
    status = status,
    comment = comment
)

fun HomeworkLog.toHomeworkLogEntity() = HomeworkLogEntity(
    id = id,
    studentId = studentId,
    timestamp = timestamp,
    homeworkType = homeworkType,
    status = status,
    comment = comment
)
