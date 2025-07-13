package com.example.behaviorlogger.db

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.example.behaviorlogger.db.dao.BehaviorLogDao
import com.example.behaviorlogger.db.dao.FurnitureItemDao
import com.example.behaviorlogger.db.dao.HomeworkLogDao
import com.example.behaviorlogger.db.dao.QuizLogDao
import com.example.behaviorlogger.db.dao.StudentDao
import com.example.behaviorlogger.db.entity.BehaviorLogEntity
import com.example.behaviorlogger.db.entity.FurnitureItemEntity
import com.example.behaviorlogger.db.entity.HomeworkLogEntity
import com.example.behaviorlogger.db.entity.QuizLogEntity
import com.example.behaviorlogger.db.entity.StudentEntity

@Database(
    entities = [
        StudentEntity::class,
        FurnitureItemEntity::class,
        BehaviorLogEntity::class,
        HomeworkLogEntity::class,
        QuizLogEntity::class
    ],
    version = 1,
    exportSchema = false
)
@TypeConverters(com.example.behaviorlogger.db.TypeConverters::class)
abstract class AppDatabase : RoomDatabase() {

    abstract fun studentDao(): StudentDao
    abstract fun furnitureItemDao(): FurnitureItemDao
    abstract fun behaviorLogDao(): BehaviorLogDao
    abstract fun homeworkLogDao(): HomeworkLogDao
    abstract fun quizLogDao(): QuizLogDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "behavior_logger_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
