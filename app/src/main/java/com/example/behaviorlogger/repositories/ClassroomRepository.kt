package com.example.behaviorlogger.repositories

import com.example.behaviorlogger.db.dao.BehaviorLogDao
import com.example.behaviorlogger.db.dao.FurnitureItemDao
import com.example.behaviorlogger.db.dao.HomeworkLogDao
import com.example.behaviorlogger.db.dao.QuizLogDao
import com.example.behaviorlogger.db.dao.StudentDao
import com.example.behaviorlogger.model.StudentItem
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.combine

class ClassroomRepository(
    private val studentDao: StudentDao,
    private val furnitureItemDao: FurnitureItemDao,
    private val behaviorLogDao: BehaviorLogDao,
    private val homeworkLogDao: HomeworkLogDao,
    private val quizLogDao: QuizLogDao
) {

    val students: Flow<List<StudentItem>> = studentDao.getAllStudents()
        .combine(behaviorLogDao.getLatestLogForEachStudent()) { students, latestBehaviors ->
            students.map { studentEntity ->
                val studentItem = studentEntity.toStudentItem()
                val latestBehavior = latestBehaviors[studentEntity.id]
                studentItem.copy(
                    lastBehavior = latestBehavior?.behavior,
                    lastBehaviorTimestamp = latestBehavior?.timestamp.toString()
                )
            }
        }

    // This is a placeholder for a real implementation
    private fun BehaviorLogDao.getLatestLogForEachStudent(): Flow<Map<Long, com.example.behaviorlogger.db.entity.BehaviorLogEntity>> {
        return kotlinx.coroutines.flow.flowOf(emptyMap())
    }
}
