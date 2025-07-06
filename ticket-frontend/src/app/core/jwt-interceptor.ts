import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core'
import { Auth } from './auth';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(Auth);
  const token = auth.currentTokenValue;

  if (token) {
    req = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${token}`)
    });
  }

  return next(req);
};
