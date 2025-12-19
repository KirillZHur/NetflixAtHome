import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';
import { AuthService } from '../../shared/services/auth.service';
import { MetricsService } from 'src/app/shared/services/metrics.service';

@Component({
  standalone: true,
  selector: 'app-auth-page',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './auth-page.component.html',
  styleUrls: ['./auth-page.component.css'],
})
export class AuthPageComponent {
  isRegister = false;
  loading = false;
  error: string | null = null;
  success: string | null = null;
  showPassword = false;

  loginForm = this.fb.group({
    login: ['', [Validators.required]],
    password: ['', [Validators.required]],
  });

  registerForm = this.fb.group({
    username: ['', [Validators.required, Validators.minLength(3)]],
    email: ['', [Validators.required, Validators.email]],
    phone: ['', [
      Validators.required,
      Validators.pattern(/^\+?[0-9]{10,15}$/) // +79991234567 или 79991234567
    ]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private metrics: MetricsService,
  ) {}

  login(): void {
    this.error = null;
    this.success = null;

    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    const login = this.loginForm.value.login!.trim();
    const password = this.loginForm.value.password!;

    this.loading = true;

    this.auth.login(login, password).pipe(
      finalize(() => (this.loading = false))
    ).subscribe({
      next: () => {
        console.log('LOGIN OK');
        this.metrics.userEvent('user_login').subscribe();
        this.router.navigateByUrl('/'); },
      error: (e) => {
        if (e?.status === 404) this.error = 'Пользователь не найден';
        else if (e?.status === 422) this.error = 'Неверный пароль';
        else if (e?.status === 409) this.error = 'Пользователь уже существует';
        else if (e?.status === 0) this.error = 'Нет соединения / CORS / прокси';
        else this.error = 'Ошибка входа (500 на сервере) — смотри логи backend';
      }
    });
  }

  register(): void {
    this.error = null;
    this.success = null;

    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    const req = {
      username: this.registerForm.value.username!.trim(),
      email: this.registerForm.value.email!.trim(),
      phone: this.registerForm.value.phone!.trim(),
      password: this.registerForm.value.password!,
    };

    this.loading = true;

    this.auth.register(req).pipe(
      finalize(() => (this.loading = false))
    ).subscribe({
      next: (ok) => {
        if (!ok) {
          this.error = 'Не удалось зарегистрироваться';
          return;
        }
        this.metrics.userEvent('user_registered').subscribe();
        this.success = 'Аккаунт создан. Теперь войдите.';
        this.isRegister = false;

        this.loginForm.patchValue({
          login: req.username,
          password: req.password,
        });
      },
      error: (e) => {
        if (e?.status === 409) this.error = 'Пользователь уже существует';
        else if (e?.status === 0) this.error = 'Нет соединения / CORS / прокси';
        else this.error = 'Ошибка регистрации (500 на сервере) — смотри логи backend';
      }
    });
  }
}
