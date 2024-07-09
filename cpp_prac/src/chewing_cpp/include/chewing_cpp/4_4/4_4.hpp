#include <iostream>

class Marine
{
    static int total_marine_num;
    const static int i = 0;
    
    int hp;
    int coord_x, coord_y;
    // int damage;
    bool is_dead;

    const int default_damage;

    public:
        Marine();
        Marine(int x, int y);
        Marine(int x, int y, int default_damage);
        
        // int attack();
        // void be_attacked(int damage_earn);
        int attack() const; 
        Marine& be_attacked(int damage_earn);
        void move(int x, int y);

        void show_status();
        static void show_total_marine();

        ~Marine(){total_marine_num--;}
};