import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { HelloController } from './hello/hello.controller';

@Module({
  imports: [],
  controllers: [AppController, HelloController],
  providers: [AppService],
})
export class AppModule {}
