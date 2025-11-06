import { Body, Controller, Post } from '@nestjs/common';
import { AuthService } from './auth.service';

@Controller('api/v1/auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('signup')
  signup(@Body() body: { email: string; password: string }) {
    return this.authService.signup(body.email, body.password);
  }

  @Post('signin')
  signin(@Body() body: { email: string; password: string }) {
    return this.authService.signin(body.email, body.password);
  }

  @Post('signout')
  signout() {
    return this.authService.signout();
  }
}
