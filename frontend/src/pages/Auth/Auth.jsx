import { createContext } from "react";
import { createAuthProvider } from "react-token-auth";
let userContext = createContext({
  access_token: null,
  role: null,
  user_name: null,
  id: null,
});
export const [useAuth, authFetch, login, logout] = createAuthProvider({
  accessTokenKey: "access_token",
  onUpdateToken: (token) =>
    fetch("/auth/refresh", {
      method: "POST",
      body: token.access_token,
    }).then((r) => r.json()),
  onHydratation: (data) => {
    userContext = createContext({
      access_token: data?.access_token,
      role: data?.role,
      user_name: data?.user_name,
      id: data?.id,
    });
  },
});
export { userContext };
