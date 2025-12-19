import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { MoviesService, FilmDto } from '../../shared/services/movies.service';

type UiFilm = FilmDto & {
  posterUrl: string;
};

@Component({
  standalone: true,
  selector: 'app-home-page',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css'],
})
export class HomePageComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  search = new FormControl('', { nonNullable: true });

  loading = false;
  error: string | null = null;

  private allFilms: UiFilm[] = [];

  films: UiFilm[] = [];

  
  private readonly mockPoster = 'https://placehold.co/240x360?text=%F0%9F%8E%AC';


  constructor(
    private movies: MoviesService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadFilms();

    this.search.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe((value) => {
        this.applySearch(value);
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  openMovie(id: string): void {
    this.router.navigate(['/movie', id]);
  }

  /*openPlayer(id: string): void {
    this.router.navigate(['/player', id]);
  }*/

  clearSearch(): void {
    this.search.setValue('');
  }

  private loadFilms(): void {
    this.loading = true;
    this.error = null;

    this.movies.getPopular(50, 1).subscribe({
      next: (items) => {
        const enriched = this.enrich(items);
        this.allFilms = enriched;
        this.films = enriched;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.error = 'Не удалось загрузить фильмы';
      },
    });
  }

  private applySearch(query: string): void {
    const q = query.trim().toLowerCase();

    if (!q) {
      this.films = this.allFilms;
      return;
    }

    this.films = this.allFilms.filter((f) =>
      f.title.toLowerCase().includes(q)
    );
  }

  private enrich(items: FilmDto[]): UiFilm[] {
    return items.map((f, i) => ({
      ...f,
      posterUrl: f.preview ||this.mockPoster,
    }));
  }
}
