import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { catchError, EMPTY, Observable } from 'rxjs';

export type FilmEventTag = 'film_visited' | 'start_watching_film' | 'finished_watching_film';
export type UserEventTag = 'user_registered' | 'user_login';

@Injectable({ providedIn: 'root' })
export class MetricsService {
  private readonly METRICS_HOST = 'http://localhost:8900';

  constructor(private http: HttpClient, private auth: AuthService) {}

  filmEvent(film_id: string, film_event_tag: FilmEventTag, event_time?: string): Observable<any> {
    const body = {
      film_id,
      film_event_tag,
      event_time: event_time ?? this.now(),
    };

    return this.http
      .post(`${this.METRICS_HOST}/film_event/`, body, { headers: this.headers() })
      .pipe(catchError(() => EMPTY)); 
  }

  userEvent(user_event_tag: UserEventTag, event_time?: string): Observable<any> {
    const body = {
      user_event_tag,
      event_time: event_time ?? this.now(),
    };

    return this.http
      .post(`${this.METRICS_HOST}/user_event/`, body, { headers: this.headers() })
      .pipe(catchError(() => EMPTY));
  }

  private headers(): HttpHeaders {
    const token = this.auth.accessToken;
    return new HttpHeaders({
      Authorization: token ?? '',
    });
  }

  // формат "YYYY-MM-DD HH:mm:ss"
  private now(): string {
    const d = new Date();
    const pad = (n: number) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  }
}
