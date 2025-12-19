import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, finalize, of, Subject, switchMap, takeUntil } from 'rxjs';
import { MoviesService, FilmWorkDto } from '../../shared/services/movies.service';
import { MetricsService } from 'src/app/shared/services/metrics.service';

@Component({
  standalone: true,
  selector: 'app-player-page',
  imports: [CommonModule],
  templateUrl: './player-page.component.html',
  styleUrls: ['./player-page.component.css'],
})
export class PlayerPageComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  loading = false;
  error: string | null = null;

  film: FilmWorkDto | null = null;

  videoUrl: string | null = null;

  readonly mockVideoUrl = 'https://www.w3schools.com/html/mov_bbb.mp4';

  isPlaying = false;

  constructor(
    private route: ActivatedRoute,
    private movies: MoviesService,
    private router: Router,
    private metrics: MetricsService,
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
      .subscribe((film) => {
        const key = film?.video;
        this.videoUrl = null;
        if (key) {
          this.movies.getVideoStream(key).subscribe({
            next: (blob) => {
              if (this.videoUrl?.startsWith('blob:')) {
                URL.revokeObjectURL(this.videoUrl);
              }
              this.videoUrl = URL.createObjectURL(blob);
            },
            error: () => {
              this.error = 'Не удалось загрузить видео';
            }
          });
        }
        this.film = film;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  play(): void {
    this.isPlaying = true;

    const filmId = this.route.snapshot.paramMap.get('id');
    if (filmId) this.metrics.filmEvent(filmId, 'start_watching_film').subscribe();

    setTimeout(() => {
      const el = document.getElementById('player-video') as HTMLVideoElement | null;
      el?.play().catch(() => {
      });
    }, 0);
  }

  onEnded(): void {
    const filmId = this.route.snapshot.paramMap.get('id');
    if (filmId) this.metrics.filmEvent(filmId, 'finished_watching_film').subscribe();
  }

  back(): void {
    this.router.navigateByUrl('/');
  }
}
