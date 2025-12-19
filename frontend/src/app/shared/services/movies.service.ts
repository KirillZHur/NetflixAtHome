import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface FilmDto {
  id: string;
  title: string;
  imdb_rating: number;
  preview: string | null;
}

export interface PersonShort {
  id: string;
  name: string;
}

export interface FilmWorkDto {
  id: string;
  imdb_rating: number;
  genres: (string | null)[];
  title: string;
  description: string;
  preview: string | null;
  video: string | null;

  directors_names: string[];
  actors_names: string[];
  writers_names: string[];

  directors: PersonShort[];
  actors: PersonShort[];
  writers: PersonShort[];
}

@Injectable({ providedIn: 'root' })
export class MoviesService {
  private readonly HOST = 'http://localhost:8002';
  private readonly API_BASE = '/content-service/api/v1/films';
  private readonly STREAM_ENDPOINT = '/content-service/api/v1/storage/stream';

  constructor(private http: HttpClient) {}

  getPopular(pageSize = 50, pageNumber = 1, sort = '-imdb_rating'): Observable<FilmDto[]> {
    const params = new HttpParams()
      .set('page_size', pageSize)
      .set('page_number', pageNumber)
      .set('sort', sort);

    return this.http.get<FilmDto[]>(this.url('/'), { params });
  }

  getById(filmId: string): Observable<FilmWorkDto> {
    return this.http.get<FilmWorkDto>(this.url(`/${encodeURIComponent(filmId)}`));
  }

  getVideoStream(key: string): Observable<Blob> {
    const params = new HttpParams().set('key', key);

    return this.http.get(`${this.HOST}${this.STREAM_ENDPOINT}`, {
      params,
      responseType: 'blob',
    });
  }

  private url(path: string): string {
    return `${this.HOST}${this.API_BASE}${path}`;
  }
}