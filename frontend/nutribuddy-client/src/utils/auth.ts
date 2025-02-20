  export const isAuthenticated = (): boolean => {
    return !!localStorage.getItem("token");  // ✅ Checks if token exists
  };

  export const logout = (): void => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    window.location.href = "/";  // ✅ Redirect to home after logout
  };

  
  export const getToken = (): string | null => {
    return localStorage.getItem("token");
  };
  
