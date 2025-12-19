import { Routes } from '@angular/router';
import { AuthPageComponent } from './pages/auth-page/auth-page.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { MoviePageComponent } from './pages/movie-page/movie-page.component';
import { PlayerPageComponent } from './pages/player-page/player-page.component';
import { authGuard } from './shared/guards/auth.guard';

export const routes: Routes = [
  { path: 'auth', component: AuthPageComponent },
  { path: '', component: HomePageComponent, canActivate: [authGuard] },
  { path: 'movie/:id', component: MoviePageComponent, canActivate: [authGuard] },
  { path: 'player/:id', component: PlayerPageComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '' },
];
