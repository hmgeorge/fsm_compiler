/* Function that does each action in this state */
void DoActions( void )
{
        int j;

        for(j = 0; j < sd[ current_state_index ].afp_length; j++ )
        {
                sd[ current_state_index ].afp[j](NULL);
                /*fp++; */
        }

return;
}

/* Function that selects the first transition that satisfies the predicate condition */
bool DoTransition( void )
{
        int i;
        TransCondStatePair * temp;
        
        temp = sd[ current_state_index ].tsp;

        for(i = 0; i < sd[ current_state_index ].tsp_length; i++ )
        {
                if( temp->p(NULL) == TRUE )
                {
                        current_state_index = temp->new_state_index;
                        return TRUE;
                }
                temp++;
        }

return FALSE;
}

int main(int argc, char ** argv)
{       

        int i;
        bool res;
        
        InitStartState( );
        
        while( 1 )
        {                
                res = DoTransition( );
                
                if ( res == FALSE )
                {
                   printf("Invalid Transistion from %s", sd[current_state_index].state_name );
                }
                else
                {
                   DoActions( );
                } 
                
                sleep( 2 );
        }

}