import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Auth {
  private authTokenSubject = new BehaviorSubject<string | null>(null);
  private readonly TOKEN_KEY = 'ticket_system_jwt';
  private isBrowser: boolean;

  constructor(private http: HttpClient, @Inject(PLATFORM_ID) platformId: Object) {
    this.isBrowser = isPlatformBrowser(platformId);

    if (this.isBrowser) {
      const storedToken = localStorage.getItem(this.TOKEN_KEY);
      if (storedToken) {
        this.authTokenSubject.next(storedToken);
      }
    }
  }

  get currentToken$(): Observable<string | null> {
    return this.authTokenSubject.asObservable();
  }

  get currentTokenValue(): string | null {
    return this.authTokenSubject.value;
  }

  login(username: string, password: string): Observable<{ access: string }> {
    return this.http.post<{ access: string }>('http://localhost:8000/api/login/', {
      username,
      password
    }).pipe(
      tap(response => {
        this.storeToken(response.access);
      })
    );
  }

  logout(): void {
    this.removeToken();
  }

  private storeToken(token: string): void {
    if (this.isBrowser) {
      localStorage.setItem(this.TOKEN_KEY, token);
    }
    this.authTokenSubject.next(token);
  }

  private removeToken(): void {
    if (this.isBrowser) {
      localStorage.removeItem(this.TOKEN_KEY);
    }
    this.authTokenSubject.next(null);
  }

  isAuthenticated(): boolean {
    return !!this.currentTokenValue;
  }
}
