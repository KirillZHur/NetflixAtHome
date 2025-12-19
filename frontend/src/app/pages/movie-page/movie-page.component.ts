import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, finalize, of, Subject, switchMap, takeUntil } from 'rxjs';
import { MoviesService, FilmWorkDto } from '../../shared/services/movies.service';
import { MetricsService } from '../../shared/services/metrics.service';

@Component({
  standalone: true,
  selector: 'app-movie-page',
  imports: [CommonModule],
  templateUrl: './movie-page.component.html',
  styleUrls: ['./movie-page.component.css'],
})
export class MoviePageComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  loading = false;
  error: string | null = null;
  film: FilmWorkDto | null = null;
  defaultPreview = "https://placehold.co/420x600?text=%F0%9F%8E%AC+Movie";

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private movies: MoviesService,
    private metrics: MetricsService
  ) {}

  ngOnInit(): void {
    //this.loading = true;

    this.route.paramMap
      .pipe(
        switchMap((pm) => {
          const id = pm.get('id');
          if (!id) {
            this.error = 'Не найден id фильма';
            return of(null);
          }

          this.metrics.filmEvent(id, 'film_visited').subscribe();

          return this.movies.getById(id).pipe(
            catchError((e) => {
              this.error = e?.status === 404 ? 'Фильм не найден' : 'Ошибка загрузки фильма';
              return of(null);
            })
          );
        }),
        finalize(() => (this.loading = false)),
        takeUntil(this.destroy$)
      )
      .subscribe((film) => (this.film = film));
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  back(): void {
    this.router.navigateByUrl('/');
  }

  watch(): void {
    if (!this.film) return;
    this.router.navigate(['/player', this.film.id]);
  }

  // чтобы красиво выводить списки через запятую
  join(arr?: string[] | null): string {
    return arr && arr.length ? arr.join(', ') : '—';
  }
}
