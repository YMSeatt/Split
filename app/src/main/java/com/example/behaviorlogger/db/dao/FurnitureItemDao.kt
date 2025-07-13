package com.example.behaviorlogger.db.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.example.behaviorlogger.db.entity.FurnitureItemEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface FurnitureItemDao {
    @Query("SELECT * FROM furniture_items")
    fun getAllFurnitureItems(): Flow<List<FurnitureItemEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertFurnitureItem(item: FurnitureItemEntity): Long

    @Update
    suspend fun updateFurnitureItem(item: FurnitureItemEntity)

    @Delete
    suspend fun deleteFurnitureItem(item: FurnitureItemEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<FurnitureItemEntity>)
}
