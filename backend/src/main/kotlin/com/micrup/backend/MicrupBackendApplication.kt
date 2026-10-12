package com.micrup.backend

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class MicrupBackendApplication

fun main(args: Array<String>) {
    runApplication<MicrupBackendApplication>(*args)
}
