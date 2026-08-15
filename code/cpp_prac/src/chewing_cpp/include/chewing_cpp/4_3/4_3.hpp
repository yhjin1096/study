#include <iostream>
#include <string.h>

class Marine
{
  //private
  int hp;
  int coord_x, coord_y;
  int damage;
  bool is_dead;
  char* name;

  public:
    Marine();// = default;
    Marine(int x, int y);
    Marine(int x, int y, const char* marine_name);  // 이름까지 지정
    ~Marine();

    int attack(); // 데미지 리턴
    void be_attacked(int damage_earn); //입는 데미지
    void move(int x, int y);

    void show_status();
};

class Photon_Cannon
{
  int hp, shield;
  int coord_x, coord_y;
  int damage;
  

  public:
  char *name;
    Photon_Cannon(int x, int y);
    Photon_Cannon(const Photon_Cannon& pc);
    Photon_Cannon(int x, int y, const char *cannon_name);
    ~Photon_Cannon();

    void show_status();
};