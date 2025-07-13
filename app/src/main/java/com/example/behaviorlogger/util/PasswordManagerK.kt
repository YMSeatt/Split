package com.example.behaviorlogger.util

import java.security.MessageDigest

class PasswordManagerK(private val settingsRepository: com.example.behaviorlogger.repositories.SettingsRepository) {

    private fun hashPassword(password: String): String {
        val digest = MessageDigest.getInstance("SHA-512")
        val hashedBytes = digest.digest(password.toByteArray())
        return hashedBytes.joinToString("") { "%02x".format(it) }
    }

    suspend fun setPassword(password: String) {
        val hash = hashPassword(password)
        settingsRepository.updateAppPasswordHash(hash)
    }

    suspend fun checkPassword(password: String): Boolean {
        // This is not a complete implementation. It needs to fetch the stored hash
        // from the settings repository.
        val storedHash = ""
        return storedHash == hashPassword(password)
    }

    suspend fun removePassword() {
        settingsRepository.updateAppPasswordHash(null)
    }
}
