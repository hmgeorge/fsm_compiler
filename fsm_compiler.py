import sys

states = []
start_state = False
transition_table = {}
action_table = {}

string_Asize ="""#define ASIZE( a ) (sizeof(a)/sizeof(a[0]))\n"""
string_bool = """typedef char bool;\n"""

string_fps="""typedef bool (* Predicate)(void *);
typedef void (* ActionCondition)(void *);\n\n"""

struct_action_func_pair = """typedef struct action_function
{
       // Predicate p;
        Action a;
}ActionFunctionPair;\n\n"""

afp_array_begin = """ActionCondition %s_afp [] = {"""
afp_array_end = """};\n"""

struct_trans_cond = """typedef struct transcond_state
{
        int new_state_index;
        Predicate p;
}TransCondStatePair;\n\n"""

trans_cond_begin = """TransCondStatePair %s_tsp [] = {"""
trans_cond_end = """};\n"""

struct_state_detail="""typedef struct state_detail
{
        char * state_name;
        TransCondStatePair * tsp;
        int tsp_length;
        ActionCondition * afp;
        int afp_length;

} State_Detail;\n\n"""

state_detail_begin = """State_Detail sd [] = {\n\n"""
state_detail_end = """};\n"""

sd_entry = """{"%s", &%s_tsp[0], ASIZE( %s_tsp ), &%s_afp[0], ASIZE( %s_afp ) },\n"""
sd_close = """\n};\n\n"""
pair="""{%s,%s},"""
func_pointer = """&%s_%s_%s"""


start_var_decl = """int current_state_index;\n"""

init_start_state = """\nvoid InitStartState( ){

        current_state_index = %d;

return;
}\n\n"""

rand_generator = """rand()%2"""

func_sign = "%s %s ( %s ) {\n"

def PrintActions( ):
  print "action table"
  print action_table
  
def PrintTransitions( ):
  print "transition table"
  print transition_table

def WriteHeaderFiles( out_f ):
  out_f.write("#include <stdio.h>\n")
  out_f.write("#include <stdlib.h>\n\n")
  

def WriteMacros( out_f ):
  out_f.write( string_Asize )
  out_f.write("#define TRUE 1\n")
  out_f.write("#define FALSE 0\n")
  out_f.write( "#define NUM_STATES " + str(len(states)) + "\n\n")
  
  out_f.write( string_bool )
  
  
def WriteTypesAndStructs( out_f ):
  out_f.write( string_fps )
 # out_f.write( struct_action_func_pair )
  out_f.write( struct_trans_cond )
  out_f.write( struct_state_detail )
  

def WriteGlobalVars( out_f ):
  out_f.write( start_var_decl )
  
def WriteTransActionFunctionStubs( out_f ):
  
  #For each transition condition, a stub has to be generated. <State>_Trans_<NewState>( )
  #transition_table[ state ][ new_state ] = condition
  
  for st,transns in transition_table.iteritems():
    for ns,cond in transns.iteritems():
      
      out_f.write( func_sign % ( "bool", st + "_Trans_" + ns, "void * param" ) )
      if ( cond != ""):
        out_f.write("\treturn " + cond + ";\n}\n\n")
      else:
        out_f.write("\treturn TRUE;\n}\n\n")
        #out_f.write("\treturn " + rand_generator + ";\n}\n\n" )
            
        
  #For each action condition, a stub has to be created. Assume function exists for action.
  #                                                             <State>_Act_<Condition>( )
  #action_table[ state ][ action ] = condition
  
  for st,acts in action_table.iteritems():
    for act,cond in acts.iteritems():
      
      out_f.write( func_sign % ( "void", st + "_Act_" + act[:act.index('(')], "void * param" ) )
      
      if(cond != ""):
        out_f.write("\tif( " + cond + " ) " )
      out_f.write( act + " ;\nreturn;\n}\n\n")
      
def WriteStructDetailsInit( out_f ):
  
 # out_f.write("void TransActionsRegister( ){\n")
  out_f.write("//Transitions and Conditions\n")
  
  #Generate The TSP for each state
  for st,transns in transition_table.iteritems():
    
    out_f.write( trans_cond_begin % st )
    
    for ns,cond in transns.iteritems():
   #   if( cond == "" ):
   #     out_f.write( pair % (ns,"NULL") )
   #   else:
       out_f.write( pair % ( states.index( ns ), func_pointer % ( st, "Trans", ns) ) )
        
                                        #"&"+cond[:cond.index('(')] ) )
                                        # note: might need change! @todo
     
    out_f.write( trans_cond_end )
  out_f.write("\n//Actions and Conditions\n")
 
  #Generate The AFP for each state
  for st,acts in action_table.iteritems():
    
    out_f.write( afp_array_begin % st )
    
    for act,cond in acts.iteritems():
      out_f.write( func_pointer % (st, "Act", act[:act.index('(')]) )
      
    out_f.write( afp_array_end )

  out_f.write("\n\n")
  out_f.write( state_detail_begin )
  
   #for each state, output the following
   #{ "<name>", <state>_tsp, ASIZE(<state>_tsp), <state>_afp, ASIZE(<state>_afp) },
  [out_f.write(sd_entry % (s,s,s,s,s) ) for s in states]
  
  out_f.write( sd_close )
  out_f.write("\n\n")
     
def WriteInitStartState( out_f ):
  out_f.write( init_start_state % ( states.index( start_state ) ) )
  
def WriteMainFunction( out_f ):
  new_f = open('main.i')
  
  for line in new_f:
    out_f.write( line )
        
  new_f.close( )
    
def WriteOutputToFile( filename ):
  
  out_f = open( filename, 'w' )
  
  WriteHeaderFiles( out_f )
  WriteMacros( out_f )
  WriteTypesAndStructs( out_f )
  WriteGlobalVars( out_f )
  WriteInitStartState( out_f )
  WriteTransActionFunctionStubs( out_f )
  WriteStructDetailsInit( out_f )
  WriteMainFunction( out_f ) 

def Start( ):
   global header_name
   global source_name
   
   #@todo: an options parser
   
   source_name = sys.argv[2] + ".c"
 #  header_name = sys.argv[2] + ".h"
   
   current_state = False
   statement = "";
   
   f = open( sys.argv[1] )
   
   for line in f:
    
     line = line.strip(' \n\t')
     
     if line == "":
       statement = ""
       continue
     
     if line.startswith("#"):
       # encountered a comment , ignore
       statement = ""
       continue
     
     if line.endswith("\\") :
       # more stuff pertaining to this line coming in the following line(s)
       statement = statement + line[:line.index("\\")] + " "
       continue
     else:
       statement = statement + line
       
     keyword = statement[:statement.index(" ")]
     statement = statement[statement.index(" "): ]
     
     if( keyword == "STATE" ):
       
       state = statement[statement.index(" "):].strip()
       current_state = state.strip()
       states.append( current_state )
       #print "processing state " + state
       transition_table[ current_state ] = { }
       action_table[ current_state ] = { }
       
     elif( keyword == "TRANSITION" ):
       
       condition = statement[statement.find("$")+1:statement.rfind("$")]
       new_state = statement[statement.rfind("$")+1:]
      # print "transition expression = " + condition
      # print "new_state = " + new_state
       
       transition_table[ current_state ][ new_state.strip() ] = condition.strip()
       
     elif( keyword == "INPUTACTION" ):
       
       condition = statement[statement.find("$")+1:statement.rfind("$")]
       action = statement[statement.rfind("$")+1:]
       #print "action expression = " + condition
       #print "action function = " + action
       
       action_table[ current_state ][ action.strip() ] = condition.strip()
       
     elif( keyword == "INITIAL" ):
       
       global start_state
       start_state = statement[statement.index(" "):].strip()
       print "start state " + start_state
       
     else:
       print "Unknown keyword"
     
     #print "current_state " + current_state
     statement = ""
     
   #end for
   
   WriteOutputToFile( source_name )
   
   print "success"
   #print states
   #print transition_table
   
   f.close()
     

if __name__ == "__main__":
    Start( )
