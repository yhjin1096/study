#include <chewing_cpp/4_3/4_3.hpp>

Marine::Marine()
{
    hp = 50;
    coord_x = coord_y = 0;
    damage = 4;
    is_dead = false;
    name = NULL;
}

Marine::Marine(int x, int y)
{
    coord_x = x;
    coord_y = y;
    hp = 40;
    damage = 4;
    is_dead = false;
    name = NULL;
}

Marine::Marine(int x, int y, const char* marine_name) {
    name = new char[strlen(marine_name) + 1]; // memory leak 발생 -> 소멸자(destuctor)에서 delete
    strcpy(name, marine_name);

    coord_x = x;
    coord_y = y;
    hp = 50;
    damage = 5;
    is_dead = false;
}

Marine::~Marine()
{
    std::cout << name << " 의 소멸자 호출 !" << std::endl;
    if(name != NULL)
        delete[] name;
}

void Marine::move(int x, int y)
{
    coord_x = x;
    coord_y = y;
}

int Marine::attack(){return damage;}

void Marine::be_attacked(int damage_earn)
{
    hp -= damage_earn;
    if(hp <= 0) is_dead = true;
}

void Marine::show_status()
{
    std::cout << " *** Marine : " << name << " ***" << std::endl;
    std::cout << " Location : ( " << coord_x << " , " << coord_y << " ) "
            << std::endl;
    std::cout << " HP : " << hp << std::endl;
}
/////////////////////////////////////////////////////////////////////////////
// 복사 생성자, 없어도 default로 복사 생성자가 있다.
Photon_Cannon::Photon_Cannon(const Photon_Cannon& pc) {
    std::cout << "복사 생성자 호출 !" << std::endl;
    hp = pc.hp;
    shield = pc.shield;
    coord_x = pc.coord_x;
    coord_y = pc.coord_y;
    damage = pc.damage;
    // name = NULL;
    name = new char(strlen(pc.name)+1);
    strcpy(name, pc.name);
}

Photon_Cannon::Photon_Cannon(int x, int y) {
  std::cout << "생성자 호출 !" << std::endl;
  hp = shield = 100;
  coord_x = x;
  coord_y = y;
  damage = 20;
  name = NULL;
}

Photon_Cannon::Photon_Cannon(int x, int y, const char *cannon_name)
{
  hp = shield = 100;
  coord_x = x;
  coord_y = y;
  damage = 20;

  name = new char[strlen(cannon_name) + 1];
  strcpy(name, cannon_name);
}

Photon_Cannon::~Photon_Cannon()
{
    std::cout << "~Photon_Cannon()" << std::endl;
    if (name) delete[] name;
}

void Photon_Cannon::show_status()
{
  std::cout << "Photon Cannon " << std::endl;
  std::cout << " Location : ( " << coord_x << " , " << coord_y << " ) "
            << std::endl;
  std::cout << " HP : " << hp << std::endl;
}