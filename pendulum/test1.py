import serial
import time
from manim import *

# Manim Scene Class
class PendulumAnimation(Scene):
    def construct(self):
        # Configure serial port
        serial_port = 'COM8'  # Replace with your ESP-32 serial port
        baud_rate = 9600
        ser = serial.Serial(serial_port, baud_rate)

        # Setup pendulum visual elements
        pivot = Dot(color=WHITE).shift(UP * 2)
        rod = Line(pivot.get_center(), pivot.get_center() + DOWN * 3, color=BLUE)
        bob = Dot(color=RED).move_to(pivot.get_center() + DOWN * 3)

        self.add(pivot, rod, bob)

        # Container for storing angle values
        angle_values = []
        start_time = time.time()

        try:
            while time.time() - start_time < 1:  # Collect data for 15 seconds
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    angle_degrees = float(line)  # Angle in degrees
                    print("Received angle:", angle_degrees)
                    angle_values.append(angle_degrees)  # Store angle in container
                time.sleep(0.001)  # Adjust as necessary to stabilize reading

        except KeyboardInterrupt:
            print("Serial communication stopped by user")

        finally:
            ser.close()

        # After collecting data, visualize it
        self.visualize_pendulum_movement(angle_values, pivot, rod, bob)

    def visualize_pendulum_movement(self, angles, pivot, rod, bob):
        # Function to animate pendulum based on stored angles
        # Convert degrees to radians for calculation
        def degrees_to_radians(degrees):
            return degrees * DEGREES

        # Animation logic based on stored angles
        for angle_degrees in angles:
            angle_radians = degrees_to_radians(angle_degrees)

            # Calculate new positions
            new_pos_bob = pivot.get_center() + DOWN * 3 * np.array([np.sin(angle_radians), -np.cos(angle_radians), 0])
            new_pos_rod_end = pivot.get_center() + DOWN * 3 * np.array([np.sin(angle_radians), -np.cos(angle_radians), 0])

            # Update positions and rotation using animations
            rod_anim = rod.animate.put_start_and_end_on(pivot.get_center(), new_pos_rod_end)
            bob_anim = bob.animate.move_to(new_pos_bob)
            bob_rotate = Rotate(bob, -angle_radians, about_point=pivot.get_center(), axis=OUT)

            # Play animations
            self.play(
                rod_anim,
                bob_anim,
                bob_rotate,
                run_time=0.1  # Adjust animation speed as needed
            )

# Main entry point
if __name__ == "__main__":
    scene = PendulumAnimation()
    scene.render()
