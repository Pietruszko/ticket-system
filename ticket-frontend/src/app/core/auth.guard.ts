import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { Auth } from './auth';

export const authGuard: CanActivateFn = () => {
  const auth = inject(Auth);
  const router = inject(Router);
  
  if (auth.isAuthenticated()) {
    return true;
  }
  
  return router.createUrlTree(['/login']);
};