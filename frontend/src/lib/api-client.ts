import { 
  LoginRequest, 
  TokenResponse, 
  User, 
  CreateUserRequest, 
  CreateUserResponse, 
  EditUserByAdminRequest, 
  EditMeRequest, 
  EditMeResponse 
} from '@/types/api';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Ключ 'token' — тот же, что читает useAuth.ts для гейта защищённых страниц.
function getStoredToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

function authHeader(): Record<string, string> {
  const token = getStoredToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handleResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get('content-type');
  const isJson = contentType && contentType.includes('application/json');
  const data = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    // Обработка ошибок согласно документации (поле detail)
    const message = data?.detail 
      ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
      : response.statusText || 'Unknown Error';
    throw new Error(message);
  }

  return data as T;
}

async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const url = `${BASE_URL}${path}`;

  const defaultOptions: RequestInit = {
    ...options,
    credentials: 'include', // Обязательно для работы с refresh_token в куках
    headers: {
      'Content-Type': 'application/json',
      ...authHeader(),
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, defaultOptions);
    return await handleResponse<T>(response);
  } catch (error) {
    console.error(`API Request Error [${path}]:`, error);
    throw error;
  }
}

// Бэкенд принимает эти поля как multipart/form-data (FastAPI Form(...)),
// а не JSON — Content-Type с boundary для FormData браузер проставляет сам.
async function apiFormRequest<T, B extends object = object>(
  path: string,
  method: string,
  body: B
): Promise<T> {
  const url = `${BASE_URL}${path}`;
  const formData = new FormData();
  for (const [key, value] of Object.entries(body as Record<string, string | number | null | undefined>)) {
    if (value !== null && value !== undefined) {
      formData.append(key, String(value));
    }
  }

  try {
    const response = await fetch(url, {
      method,
      credentials: 'include',
      headers: authHeader(),
      body: formData,
    });
    return await handleResponse<T>(response);
  } catch (error) {
    console.error(`API Request Error [${path}]:`, error);
    throw error;
  }
}

export const apiClient = {
  // Auth
  login: (body: LoginRequest) => 
    apiRequest<TokenResponse>('/api/v1/login', { method: 'POST', body: JSON.stringify(body) }),

  refresh: () => 
    apiRequest<TokenResponse>('/api/v1/refresh', { method: 'POST' }),

  logout: () =>
    apiRequest<{ detail: string }>('/api/v1/logout', { method: 'POST' }),

  getUserCredentials: () => 
    apiRequest<User>('/api/v1/user-credentials'),

  // Users Management
  getUsers: () => 
    apiRequest<User[]>('/api/v1/users/'),

  getUserById: (userId: number) => 
    apiRequest<User>(`/api/v1/users/${userId}`),

  createUser: (body: CreateUserRequest) =>
    apiFormRequest<CreateUserResponse>('/api/v1/users/create_user', 'POST', body),

  editUser: (userId: number, body: EditUserByAdminRequest) =>
    apiFormRequest<User>(`/api/v1/users/${userId}/edit`, 'PATCH', body),

  editMe: (body: EditMeRequest) =>
    apiFormRequest<EditMeResponse>('/api/v1/users/me/edit', 'PATCH', body),

  deleteUser: (userId: number) =>
    apiRequest<string>(`/api/v1/users/${userId}/delete-account`, { method: 'DELETE' }),
};
