import { fetcher } from '@/contents/api/fetcher';
import type { DinoStatus } from '@/contents/api/types';

type RegisterParams = {
  github_name: string;
  color: DinoStatus['color'];
  level: DinoStatus['level'];
};

export type RegisterResponse = {
  status: DinoStatus;
};

/**
 *  POST /register
 */
export const post = (params: RegisterParams) =>
  fetcher<RegisterResponse>('register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  });
