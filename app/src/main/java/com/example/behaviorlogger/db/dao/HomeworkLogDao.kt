package com.example.behaviorlogger.db.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.behaviorlogger.db.entity.HomeworkLogEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface HomeworkLogDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLog(log: HomeworkLogEntity)

    @Query("SELECT * FROM homework_logs WHERE studentId = :studentId ORDER BY timestamp DESC")
    fun getLogsForStudent(studentId: Long): Flow<List<HomeworkLogEntity>>

    @Query("SELECT * FROM homework_logs WHERE studentId = :studentId ORDER BY timestamp DESC LIMIT 1")
    fun getLatestLogForStudent(studentId: Long): Flow<HomeworkLogEntity?>
}
