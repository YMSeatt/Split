package com.example.behaviorlogger.db.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.behaviorlogger.db.entity.BehaviorLogEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface BehaviorLogDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLog(log: BehaviorLogEntity)

    @Query("SELECT * FROM behavior_logs WHERE studentId = :studentId ORDER BY timestamp DESC")
    fun getLogsForStudent(studentId: Long): Flow<List<BehaviorLogEntity>>

    @Query("SELECT * FROM behavior_logs WHERE studentId = :studentId ORDER BY timestamp DESC LIMIT 1")
    fun getLatestLogForStudent(studentId: Long): Flow<BehaviorLogEntity?>
}
