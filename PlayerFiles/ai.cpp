#include "basic.h"
#include <stdio.h>

game_info info;
char teamName[20]="player";

int GetHeroType()
{
	return ASSASSIN;
}

Command AI_main()
{
	Command cmd;
	//ѡ��������д�Լ���AI������
	cmd.order = attack;
	cmd.destination = info.soldier[info.move_id][info.team_number].pos;
	cmd.target_id = 0;
	return cmd;
}