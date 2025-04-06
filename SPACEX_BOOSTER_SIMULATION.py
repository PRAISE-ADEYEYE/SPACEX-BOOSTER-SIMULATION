from vpython import *
import random  # Added for star background effects

# --------------------------
# Scene Setup
# --------------------------
scene = canvas(title="SpaceX Booster Catch – Enhanced Simulation",
               width=1200, height=600, background=color.black)
scene.center = vector(0, 50, 0)

# Ground, Launch Pad, and Tower with Mechanical Arms
ground = box(pos=vector(0, -1, 0), size=vector(300, 2, 300), color=color.green)
launch_pad = box(pos=vector(0, 0, 0), size=vector(40, 1, 40), color=color.gray(0.3))
tower = box(pos=vector(0, 60, -90), size=vector(30, 120, 30), color=color.gray(0.5))

# Mechanical Arms for Booster Catch
arm_left = box(pos=vector(-25, 110, -90), size=vector(5, 40, 5), color=color.red, visible=True)
arm_right = box(pos=vector(25, 110, -90), size=vector(5, 40, 5), color=color.red, visible=True)

# Telemetry Panel (anchored at bottom left)
telemetry = label(pos=vector(-140, -70, 0), text="", height=12, box=False,
                  color=color.white, align="left", font="monospace")

# Countdown Label (centered at top)
countdown_label = label(pos=vector(0, 120, 0), text="", height=20, box=False, color=color.yellow)

# --------------------------
# Create Rocket & Booster Objects
# --------------------------
# Main Rocket (upper stage) with flame effect
rocket = cylinder(pos=vector(0, 0, 0), axis=vector(0, 30, 0), radius=2, color=color.white)
rocket_flame = cone(pos=rocket.pos, axis=vector(0, -10, 0),
                    radius=3, color=color.orange, visible=False)

# Booster (initially hidden, attached to rocket)
booster = cylinder(pos=rocket.pos - vector(0, 18, 0), axis=vector(0, 20, 0),
                   radius=2.5, color=color.blue, visible=False)

# --------------------------
# Additional Enhancements and Details
# --------------------------
# Enhance the rocket shape by adding a cone tip and fins for a more realistic look.
rocket_tip = cone(pos=rocket.pos + rocket.axis, axis=vector(0, 5, 0),
                  radius=2.5, color=color.red)

# Create rocket fins (left, right, top, and bottom) to improve the rocket shape.
fin_left = box(pos=rocket.pos + vector(-2.5, 10, 0), size=vector(0.5, 3, 1.5), color=color.white)
fin_right = box(pos=rocket.pos + vector(2.5, 10, 0), size=vector(0.5, 3, 1.5), color=color.white)
fin_top = box(pos=rocket.pos + vector(0, 10, -2.5), size=vector(1.5, 3, 0.5), color=color.white)
fin_bottom = box(pos=rocket.pos + vector(0, 10, 2.5), size=vector(1.5, 3, 0.5), color=color.white)

# Enhanced Launch Pad: Create an additional, more prominent launch pad in front.
enhanced_launch_pad = box(pos=vector(0, 0, 20), size=vector(45, 1, 45), color=color.white, opacity=0.5)
launch_pad_ring = ring(pos=enhanced_launch_pad.pos, axis=vector(0, 1, 0), radius=23, thickness=1, color=color.yellow)

# Add ambient light for better overall visualization.
distant_light(direction=vector(0, -1, -1), color=color.gray(0.7))

# Add a simple background star field for extra visual appeal.
for i in range(20):
    sphere(pos=vector(random.uniform(-150, 150), random.uniform(150, 300), random.uniform(-150, -50)),
           radius=0.5, color=color.white, emissive=True)

# Extra decorative label for the simulation header.
header_label = label(pos=vector(0, 130, 0), text="Welcome to the Enhanced Booster Catch Simulation",
                     height=16, box=False, color=color.cyan)

# --------------------------
# Simulation Parameters
# --------------------------
dt = 0.01
t = 0
rocket_velocity = vector(0, 0, 0)
booster_velocity = vector(0, 0, 0)
fuel = 100.0
thrust = 5000.0  # Simplified thrust value
mass = 100.0  # Simplified mass
g = 9.81

# State flags
booster_separated = False
catch_sequence = False
booster_caught = False

# --------------------------
# Countdown Sequence
# --------------------------
for i in range(10, 0, -1):
    countdown_label.text = f"Launch in {i}..."
    rate(1)
countdown_label.text = "Liftoff!"
rate(2)
countdown_label.visible = False

# --------------------------
# Main Simulation Loop
# --------------------------
while True:
    rate(100)  # control simulation speed
    t += dt

    # --- Update Main Rocket (Ascending) ---
    if fuel > 0:
        # Apply thrust; while fuel lasts, show flame and accelerate rocket
        acceleration = vector(0, thrust / mass - g, 0)
        rocket_flame.visible = True
        fuel -= 0.05
    else:
        acceleration = vector(0, -g, 0)
        rocket_flame.visible = False

    rocket_velocity += acceleration * dt
    rocket.pos += rocket_velocity * dt
    rocket_flame.pos = rocket.pos - vector(0, 5, 0)

    # --- Update Additional Rocket Details ---
    # Keep the refined rocket tip and fins attached to the main rocket body.
    rocket_tip.pos = rocket.pos + rocket.axis
    fin_left.pos = rocket.pos + vector(-2.5, 10, 0)
    fin_right.pos = rocket.pos + vector(2.5, 10, 0)
    fin_top.pos = rocket.pos + vector(0, 10, -2.5)
    fin_bottom.pos = rocket.pos + vector(0, 10, 2.5)

    # --- Update Enhanced Launch Pad ---
    # Ensure the enhanced launch pad ring stays aligned with the pad.
    launch_pad_ring.pos = enhanced_launch_pad.pos

    # --- Update Telemetry ---
    telemetry.text = (f"Time: {t:.2f} s\n"
                      f"Rocket Altitude: {rocket.pos.y:.2f} m\n"
                      f"Velocity: {rocket_velocity.y:.2f} m/s\n"
                      f"Fuel: {max(fuel, 0):.1f}%")

    # --- Booster Separation ---
    if (rocket.pos.y >= 100) and (not booster_separated):
        booster_separated = True
        booster.visible = True
        # Detach booster: position it slightly below the rocket and inherit part of its velocity
        booster.pos = rocket.pos - vector(0, 18, 0)
        booster_velocity = rocket_velocity * 0.8

    # --- Booster Descent (Controlled Reentry) ---
    if booster_separated and (not booster_caught):
        # Booster free-fall descent until entering landing zone (around 60 m altitude)
        if booster.pos.y > 60:
            booster_velocity += vector(0, -g, 0) * dt
            booster.pos += booster_velocity * dt
        else:
            # In landing zone: simulate retro-thrust deceleration for a soft landing
            if booster_velocity.y < -2:
                booster_velocity.y += 0.2  # retro-burn effect
            booster.pos += booster_velocity * dt
            # Once low enough, initiate catch sequence
            if booster.pos.y <= 60:
                catch_sequence = True

    # --- Catch Sequence: Extend Mechanical Arms ---
    if catch_sequence and (not booster_caught):
        arm_left.visible = True
        arm_right.visible = True
        # Animate arms moving inward toward the catch point (centered at x=0)
        if arm_left.pos.x < -2:
            arm_left.pos.x += 0.3
        if arm_right.pos.x > 2:
            arm_right.pos.x -= 0.3
        # When arms are close, complete the catch
        if abs(arm_left.pos.x) < 2 and abs(arm_right.pos.x) < 2:
            booster_caught = True
            catch_sequence = False

    # --- Booster Caught: Snap Booster to Tower Catch Point ---
    if booster_caught:
        booster.pos = vector(0, 60, -90)  # attach booster to tower's catch point
        booster_velocity = vector(0, 0, 0)
        telemetry.text += "\nBooster Caught!"

    # --- End Condition: Once rocket flies off-screen and booster is caught, end simulation ---
    if (rocket.pos.y > 300) and booster_caught:
        break

    # --------------------------
    # Extra Visual Updates (Optional)
    # --------------------------
    # For additional immersion, we can slowly rotate the header label.
    header_label.rotate(angle=0.005, axis=vector(0, 1, 0), origin=header_label.pos)

    # Slight flicker for the rocket flame to simulate dynamic combustion.
    if rocket_flame.visible:
        rocket_flame.radius = 3 + 0.5 * sin(10 * t)

    # Extra delay to see details in slow-motion if needed (comment out for real-time simulation)
    # rate(150)

    # Update the scene background color gradually (optional visual effect)
    # (This can add an evolving feel to the simulation over time)
    scene.background = vector(0, 0, 0.1 + 0.1 * sin(t / 10))

    # End of loop extra comments:
    # (The simulation loop continuously updates rocket dynamics, the enhanced visual details,
    #  and the interactions between the rocket, booster, and mechanical arms.)

# --------------------------
# Simulation Ended
# --------------------------
# Final message after simulation ends.
final_message = label(pos=vector(0, rocket.pos.y, 0),
                      text="Simulation Complete - Booster Successfully Caught!",
                      height=20, box=True, color=color.green)

# Additional pause to view the final state
sleep(3)

# End of code.
