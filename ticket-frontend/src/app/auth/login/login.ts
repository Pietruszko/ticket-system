import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Auth } from '../../core/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  form: FormGroup;
  error = '';

  constructor(private fb: FormBuilder, private auth: Auth, private router: Router) {
    this.form = this.fb.group({
      username: [''],
      password: ['']
    });
  }

  login() {
    const { username, password } = this.form.value;
    this.auth.login(username, password).subscribe({
      next: () => this.router.navigate(['/tickets']),
      error: () => this.error = 'Login failed. Please try again.'
    });
  }
}
