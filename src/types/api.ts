export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  name: string;
  surname: string;
  patronymic: string | null;
  email: string;
  role: string;
  is_active: boolean;
}

export interface CreateUserRequest {
  name: string;
  surname: string;
  patronymic?: string | null;
  email: string;
  password: string;
  password_confirm: string;
}

export interface CreateUserResponse {
  user: User;
  token_info: TokenResponse;
}

export interface EditUserByAdminRequest {
  name: string;
  surname: string;
  role: string;
  patronymic?: string | null;
}

export interface EditMeRequest {
  name: string;
  surname: string;
  patronymic?: string | null;
}

export interface EditMeResponse {
  name: string;
  surname: string;
  patronymic?: string | null;
}

export interface ApiError {
  detail: string | Array<{ msg: string; loc: string[] }>;
}
