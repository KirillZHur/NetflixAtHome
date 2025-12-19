import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  phone: string;
  password: string;
}


@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly HOST = 'http://localhost:8001';
  private readonly API_BASE = '/auth-service/api/v1';
  private readonly AUTH_PREFIX = '/auth';
  private readonly TOKEN_PREFIX = '/token';

  private readonly ACCESS_KEY = 'access_token';
  private readonly REFRESH_KEY = 'refresh_token';

  constructor(private http: HttpClient) {}

  get accessToken(): string | null {
    return localStorage.getItem(this.ACCESS_KEY);
  }
  get refreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_KEY);
  }

  login(usernameOrEmail: string, password: string): Observable<TokenResponse> {
    return this.http
      .post<TokenResponse>(this.url(`${this.AUTH_PREFIX}/login`), {
        username: usernameOrEmail,
        password,
      })
      .pipe(
        tap((tokens) => {
          if (tokens?.access_token) localStorage.setItem(this.ACCESS_KEY, tokens.access_token);
          if (tokens?.refresh_token) localStorage.setItem(this.REFRESH_KEY, tokens.refresh_token);
        })
      );
  }

  register(req: RegisterRequest): Observable<boolean> {
    return this.http.post<boolean>(this.url(`${this.AUTH_PREFIX}/register`), req);
  }

  refreshAccessToken(): Observable<{ access_token: string }> {
    const refresh = this.refreshToken;
    if (!refresh) throw new Error('No refresh token');

    const headers = new HttpHeaders().set('Authorization', `Bearer ${refresh}`);
    return this.http
      .post<{ access_token: string }>(this.url(`${this.TOKEN_PREFIX}/refresh_access_token`), {}, { headers })
      .pipe(tap((res) => {
        if (res?.access_token) localStorage.setItem(this.ACCESS_KEY, res.access_token);
      }));
  }

  logout(): Observable<any> {
    return this.http.post(this.url(`${this.AUTH_PREFIX}/logout`), {}).pipe(
      tap(() => this.clearTokens())
    );
  }

  clearTokens(): void {
    localStorage.removeItem(this.ACCESS_KEY);
    localStorage.removeItem(this.REFRESH_KEY);
  }

  private url(path: string): string {
    return `${this.HOST}${this.API_BASE}${path}`;
  }
}
