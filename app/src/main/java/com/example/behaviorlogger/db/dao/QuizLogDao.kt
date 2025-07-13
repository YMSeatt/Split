package com.example.behaviorlogger.db.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.behaviorlogger.db.entity.QuizLogEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface QuizLogDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLog(log: QuizLogEntity)

    @Query("SELECT * FROM quiz_logs WHERE studentId = :studentId ORDER BY timestamp DESC")
    fun getLogsForStudent(studentId: Long): Flow<List<QuizLogEntity>>

    @Query("SELECT * FROM quiz_logs WHERE studentId = :studentId ORDER BY timestamp DESC LIMIT 1")
    fun getLatestLogForStudent(studentId: Long): Flow<QuizLogEntity?>
}
