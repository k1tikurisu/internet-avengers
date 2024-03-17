import * as registerAPI from '@/contents/api/register';
import type { DinoStatus } from '@/contents/api/types';
import { getUserName } from '@/contents/utils/get-user-name';
import { type MouseEventHandler, useState } from 'react';
import { Egg } from './egg/egg';
import { StartButton } from './start-button/start-button';

export const DinoSelection = () => {
  /**
   * State
   */
  const [disabled, setDisabled] = useState(false);
  const [color, _setColor] = useState<DinoStatus['color']>('green');

  /**
   * Handler
   */
  const onClickStartButtonHandler: MouseEventHandler<HTMLButtonElement> = async () => {
    try {
      setDisabled(true);

      await registerAPI.post({ github_name: getUserName(), color });
    } catch {
      /** エラーハンドリング */
    } finally {
      setDisabled(false);
    }
  };

  return (
    <div>
      <Egg color={color} />
      <StartButton onClick={onClickStartButtonHandler} disabled={disabled} />
    </div>
  );
};
