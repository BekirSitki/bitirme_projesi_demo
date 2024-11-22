import neat
import os
import pickle
import math

from pacman import *
import pacman

def customStartGame(net, genome):

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)


  p_turn = 0
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0


  # Create the player paddle object
  Pacman = Player( w, p_h, "images/pacman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Blinky=Ghost( w, b_h, "images/Blinky.png" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "images/Pinky.png" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky=Ghost( i_w, m_h, "images/Inky.png" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde=Ghost( c_w, m_h, "images/Clyde.png" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0

  steps_taken = 0
  tick = 0

  done = False

  i = 0

  while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
      output = net.activate(  # nqa
            (
                len(pygame.sprite.spritecollide( Player( Pacman.rect.left - 30, Pacman.rect.top + 0, "images/pacman.png" ), block_list, False)),
                len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 30, Pacman.rect.top + 0, "images/pacman.png" ), block_list, False)),
                len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 0, Pacman.rect.top - 30, "images/pacman.png" ), block_list, False)),
                len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 0, Pacman.rect.top + 30, "images/pacman.png" ), block_list, False)),
                
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left - 60, Pacman.rect.top + 0, "images/pacman.png" ), monsta_list, False)) else 0,
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 60, Pacman.rect.top + 0, "images/pacman.png" ), monsta_list, False)) else 0,
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 0, Pacman.rect.top - 60, "images/pacman.png" ), monsta_list, False)) else 0,
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 0, Pacman.rect.top + 60, "images/pacman.png" ), monsta_list, False)) else 0,
                
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left - 30, Pacman.rect.top + 0, "images/pacman.png" ), wall_list, False)) else 0,
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 30, Pacman.rect.top + 0, "images/pacman.png" ), wall_list, False)) else 0,
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 0, Pacman.rect.top - 30, "images/pacman.png" ), wall_list, False)) else 0,
                1 if len(pygame.sprite.spritecollide( Player( Pacman.rect.left + 0, Pacman.rect.top + 30, "images/pacman.png" ), wall_list, False)) else 0,
                
                # Pacman.rect.left,
                # Pacman.rect.top,
                # 
                # Pinky.rect.left,
                # Pinky.rect.top,
                # 
                # Blinky.rect.left,
                # Blinky.rect.top,
                # 
                # Inky.rect.left,
                # Inky.rect.top,
                # 
                # Clyde.rect.left,
                # Clyde.rect.top,
            )
        )
      decision = output.index(max(output))
      if decision == 0:
        Pacman.changespeed(-30,0)
      elif decision == 1:
        Pacman.changespeed(30,0)
      elif decision == 2:
        Pacman.changespeed(0,-30)
      elif decision == 3:
        Pacman.changespeed(0,30)

      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      did_move = Pacman.update(wall_list,gate)
      if did_move:
        steps_taken += 1

      if decision == 0:
        Pacman.changespeed(30,0)
      elif decision == 1:
        Pacman.changespeed(-30,0)
      elif decision == 2:
        Pacman.changespeed(0,30)
      elif decision == 3:
        Pacman.changespeed(0,-30)

      returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      p_turn = returned[0]
      p_steps = returned[1]
      Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      Pinky.update(wall_list,False)

      returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      b_turn = returned[0]
      b_steps = returned[1]
      Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      Blinky.update(wall_list,False)

      returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      i_turn = returned[0]
      i_steps = returned[1]
      Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      Inky.update(wall_list,False)

      returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      c_turn = returned[0]
      c_steps = returned[1]
      Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      Clyde.update(wall_list,False)

      # See if the Pacman block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
       
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [10, 10])

      if score == bll:
        calculate_fitness(genome, steps_taken, score, tick)
        break
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if monsta_hit_list:
        calculate_fitness(genome, steps_taken, score, tick)
        break
           
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      tick += 1
      clock.tick(30)


def calculate_fitness(genome, steps_taken, score, tick):
    if score == 0:
        return
    genome.fitness += score * 50 + math.sqrt(tick) + math.sqrt(steps_taken)
    print(f"Steps taken: {steps_taken}   Tick: {tick}   Score: {score}   Fitness: {genome.fitness}")
    # genome.fitness += math.sqrt(steps_taken / 10)
    # genome.fitness += math.sqrt(tick / 10)
    pass


def AI_play(genome, config):
   net = neat.nn.FeedForwardNetwork.create(genome, config)
   customStartGame(net, genome)


def train_ai(genomes, config):
   for genome_id, genome in genomes:
      genome.fitness = 0
      AI_play(genome, config)
      pass


def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint_9500fp_190p')
    # p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(50))  # save the nn every 50 generation

    winner = p.run(train_ai)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    # game = PongGame(window, width, height)
    AI_play(winner, config)


def test_best_of_one_generation(config, checkpoint_name):
    p = neat.Checkpointer.restore_checkpoint(checkpoint_name)
    population = p.population

    # Find the genome with the highest fitness
    best_genome_id, best_genome = max(population.items(), key=lambda item: item[1].fitness if item[1].fitness is not None else float('-inf'))

    with open(f"{checkpoint_name}.pickle", "wb") as f:
        pickle.dump(best_genome, f)

    # game = PongGame(window, width, height)
    AI_play(best_genome, config)




pacman.customStartGame = customStartGame

def run_AI():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # run_neat(config)
    # test_best(config)
    test_best_of_one_generation(config, "neat-checkpoint_9500fp_190p")
    # pacman.customStartGame()

if __name__ == "__main__":
    run_AI()