/**
 * Simple authentication service for development.
 * In production, this should be replaced with Better Auth integration.
 */

/**
 * Create a test user and get a JWT token.
 * For development purposes only.
 */
export async function devLogin(): Promise<string> {
  // For development, we'll create a simple mock token
  // In a real app, this would call the Better Auth login endpoint

  // Generate a test user ID
  const testUserId = localStorage.getItem('test_user_id') || crypto.randomUUID();
  localStorage.setItem('test_user_id', testUserId);

  // Create a mock JWT token (this is for development only)
  // The backend middleware will need to be updated to handle this or accept a test mode
  const mockToken = `dev-token-${testUserId}`;

  localStorage.setItem('auth_token', mockToken);
  localStorage.setItem('user_id', testUserId);

  return mockToken;
}

/**
 * Check if user is authenticated.
 */
export function isAuthenticated(): boolean {
  const token = localStorage.getItem('auth_token');
  const userId = localStorage.getItem('user_id');

  // Both token and user ID must exist for valid authentication
  return !!(token && userId);
}

/**
 * Clear all authentication data (for logout or fresh start).
 */
export function clearAuth(): void {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_id');
  localStorage.removeItem('test_user_id');
  localStorage.removeItem('current_conversation_id');
  localStorage.removeItem('current_conversation_messages');
}

/**
 * Logout user.
 */
export function logout(): void {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_id');
  localStorage.removeItem('current_conversation_id');
  localStorage.removeItem('current_conversation_messages');
}

/**
 * Get current user ID.
 */
export function getUserId(): string | null {
  return localStorage.getItem('user_id');
}
