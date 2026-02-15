import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(private prisma: PrismaClient, private jwt: JwtService) {}

  async signup(email: string, password: string) {
    const hashed = await bcrypt.hash(password, 10);
    const user = await this.prisma.user.create({
      data: { email, password: hashed },
    });
    return { message: 'User registered successfully', user };
  }

  async signin(email: string, password: string) {
    const user = await this.prisma.user.findUnique({ where: { email } });

    if (!user) return { error: 'User not found' };

    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) return { error: 'Incorrect Password' };

    const token = this.jwt.sign({ sub: user.id, email: user.email });
    return { message: 'Login successful', token };
  }

  async signout() {
    return { message: 'Signout successful (handled on client side)' };
  }
}
