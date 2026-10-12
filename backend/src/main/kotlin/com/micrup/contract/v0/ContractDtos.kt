// Generated from docs/api/openapi.yaml; do not edit by hand.
// Run: python tools/api/generate_contract_dtos.py
// Transport shapes only. Constraints, auth and business rules are not implemented here.
// Optional request fields represented by null must be omitted unless their schema is nullable.
package com.micrup.contract.v0

enum class Currency {
    RUB
}

enum class ProjectType {
    BOT, WEB_SERVICE, MOBILE_APP, OTHER
}

enum class PublicationStatus {
    DRAFT, PENDING_REVIEW, REJECTED, PUBLISHED, ARCHIVED
}

enum class ErrorCode {
    INVALID_REQUEST, UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, CONFLICT, INTERNAL_ERROR
}

data class Money(
    val amountMinor: Long,
    val currency: Currency,
)

data class Price(
    val amountMinor: Long,
    val currency: Currency,
)

data class Technology(
    val id: String,
    val name: String,
    val slug: String,
)

data class ProjectMetrics(
    val periodStart: String,
    val periodEnd: String,
    val revenue: Money? = null,
    val expenses: Money? = null,
    val payingUserCount: Int? = null,
)

data class SellerProfile(
    val userId: String,
    val displayName: String,
    val bio: String?,
)

data class UserProfile(
    val userId: String,
    val displayName: String,
    val bio: String?,
)

data class ProfileInput(
    val displayName: String,
    val bio: String? = null,
)

data class ViewEventInput(
    val eventId: String,
)

data class FieldError(
    val field: String,
    val message: String,
)

data class ApiError(
    val code: ErrorCode,
    val message: String,
    val fieldErrors: List<FieldError>,
    val traceId: String,
)

data class Health(
    val status: String,
)

data class ProjectSummary(
    val id: String,
    val title: String,
    val type: ProjectType,
    val askingPrice: Price,
    val shortDescription: String,
    val technologies: List<Technology>,
    val supportHoursPerWeek: Double,
    val publishedAt: String,
)

data class ProjectDetails(
    val id: String,
    val title: String,
    val type: ProjectType,
    val askingPrice: Price,
    val shortDescription: String,
    val technologies: List<Technology>,
    val supportHoursPerWeek: Double,
    val publishedAt: String,
    val description: String,
    val seller: SellerProfile,
    val saleReason: String?,
    val transferredAssets: List<String>,
    val metrics: ProjectMetrics?,
)

data class ProjectDraftInput(
    val title: String? = null,
    val type: ProjectType? = null,
    val askingPrice: Price? = null,
    val shortDescription: String? = null,
    val description: String? = null,
    val technologyIds: List<String>? = null,
    val supportHoursPerWeek: Double? = null,
    val saleReason: String? = null,
    val transferredAssets: List<String>? = null,
    val metrics: ProjectMetrics? = null,
)

data class ProjectDraft(
    val id: String,
    val ownerId: String,
    val publicationStatus: PublicationStatus,
    val createdAt: String,
    val updatedAt: String,
    val rejectionReason: String? = null,
    val title: String? = null,
    val type: ProjectType? = null,
    val askingPrice: Price? = null,
    val shortDescription: String? = null,
    val description: String? = null,
    val technologyIds: List<String>? = null,
    val supportHoursPerWeek: Double? = null,
    val saleReason: String? = null,
    val transferredAssets: List<String>? = null,
    val metrics: ProjectMetrics? = null,
)

data class ProjectPage(
    val items: List<ProjectSummary>,
    val page: Int,
    val size: Int,
    val totalElements: Long,
    val totalPages: Int,
    val hasNext: Boolean,
)
