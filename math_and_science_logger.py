import textwrap

def generate_explanation(title, topic, derivation):
    """
    Formats the title, topic explanation, and derivation into a log-ready string.
    Uses LaTeX for all mathematical notation.
    """
    separator = "=" * 60
    content = f"{separator}\n"
    content += f"TOPIC: {title}\n"
    content += f"{separator}\n\n"
    content += "### EXPLANATION ###\n"
    content += textwrap.fill(topic, width=80)
    content += "\n\n"
    content += "### DERIVATION/PROOF (Conceptual or Algebraic) ###\n"
    content += derivation
    content += "\n"
    return content

def explain_phi():
    """Explains the Golden Ratio (phi) and its derivation."""
    title = "The Golden Ratio (Phi) - $\\phi \\approx 1.6180339887$"
    topic = (
        "The Golden Ratio, represented by the Greek letter $\\phi$ (phi), is an irrational number "
        "that appears throughout geometry, art, architecture, and nature. It is defined as "
        "the ratio of a line segment cut into two pieces of different lengths, such that "
        "the ratio of the whole segment to the longer segment is equal to the ratio of "
        "the longer segment to the shorter segment."
    )
    derivation = textwrap.dedent("""
    1. Define the relationship: Let the longer segment be '$a$' and the shorter be '$b$'.
       The Golden Ratio $\\phi$ is defined by the equation:
       $$\\frac{a+b}{a} = \\frac{a}{b} = \\phi$$

    2. Separate the fraction:
       $$\\frac{a}{a} + \\frac{b}{a} = \\phi$$
       $$1 + \\frac{b}{a} = \\phi$$

    3. Substitute the ratio: Since $\\frac{a}{b} = \\phi$, it follows that $\\frac{b}{a} = \\frac{1}{\\phi}$.
       $$1 + \\frac{1}{\\phi} = \\phi$$

    4. Rearrange into a quadratic equation by multiplying the entire equation by $\\phi$:
       $$\\phi + 1 = \\phi^2$$
       $$\\phi^2 - \\phi - 1 = 0$$

    5. Solve using the Quadratic Formula (choosing the positive root, as length must be positive):
       $$\\phi = \\frac{-(-1) + \\sqrt{(-1)^2 - 4(1)(-1)}}{2(1)}$$
       $$\\phi = \\frac{1 + \\sqrt{1 + 4}}{2}$$
       $$\\phi = \\frac{1 + \\sqrt{5}}{2} \\approx 1.6180339887$$
    """)
    return generate_explanation(title, topic, derivation)

def explain_emc2():
    """Explains mass-energy equivalence (E=mc^2) and its conceptual derivation."""
    title = "Mass-Energy Equivalence: $E = mc^2$"
    topic = (
        "Einstein's famous equation is the most celebrated result of his 1905 theory of Special "
        "Relativity. It states that mass ($m$) and energy ($E$) are interchangeable; they are "
        "different forms of the same thing. The factor $c^2$ (the speed of light squared) "
        "shows the immense amount of energy contained in even a small amount of mass."
    )
    derivation = textwrap.dedent("""
    The full derivation requires calculus and principles of Special Relativity, but we can look
    at the fundamental equation for relativistic energy ($E$) for a moving body with velocity ($v$):
    $$E = \\frac{m_0 c^2}{\\sqrt{1 - \\frac{v^2}{c^2}}}$$
    Where $m_0$ is the rest mass, and $c$ is the speed of light.

    1. **Taylor Series Expansion:** For small velocities ($v \\ll c$), the term $\\frac{1}{\\sqrt{1 - \\frac{v^2}{c^2}}}$
       can be approximated using a Taylor series expansion:
       $$\\frac{1}{\\sqrt{1 - x}} \\approx 1 + \\frac{1}{2}x + \\frac{3}{8}x^2 + \\dots$$
       Substituting $x = \\frac{v^2}{c^2}$:
       $$\\frac{1}{\\sqrt{1 - \\frac{v^2}{c^2}}} \\approx 1 + \\frac{1}{2}\\frac{v^2}{c^2} + \\dots$$

    2. **Substituting the Approximation back into the Energy Equation:**
       $$E \\approx m_0 c^2 \\left( 1 + \\frac{1}{2}\\frac{v^2}{c^2} \\right)$$
       $$E \\approx m_0 c^2 + \\frac{1}{2}m_0 v^2$$

    3. **Interpretation:**
       * The term $E_0 = m_0 c^2$ is the **Rest Energy**, the energy the object possesses purely because of its mass, even when stationary ($v=0$).
       * The term $KE = \\frac{1}{2}m_0 v^2$ is the classical **Kinetic Energy**.
       * The equation shows that the total energy ($E$) is the sum of the rest energy and the kinetic energy. The fundamental relationship $E = mc^2$ is the rest energy component.
    """)
    return generate_explanation(title, topic, derivation)

def explain_euler_polyhedron():
    """Explains Euler's formula for polyhedra and its conceptual proof."""
    title = "Euler's Polyhedron Formula: $F - E + V = 2$"
    topic = (
        "Euler's formula is a fundamental theorem in topology, specifically dealing with "
        "polyhedra (three-dimensional shapes with flat faces). It states that for any "
        "simple, convex polyhedron (one without holes), the number of Faces ($F$) minus "
        "the number of Edges ($E$) plus the number of Vertices ($V$) must always equal 2. "
        "This number (2) is known as the Euler characteristic of the sphere."
    )
    derivation = textwrap.dedent("""
    The common conceptual proof involves projecting the polyhedron onto a plane, turning it
    into a planar graph, and incrementally simplifying that graph.

    1. **Flattening:** Imagine removing one face from the polyhedron and stretching the rest of the surface
       flat onto a plane. The edges and vertices now form a **planar graph**. The faces are the
       regions of this graph, plus the face that was removed (the outside region).

    2. **Triangulation (Edges/Faces Step):** Starting with a face that is not a triangle (e.g., a square),
       draw a diagonal edge across it. This action increases the number of edges ($E$) by 1 and the
       number of faces ($F$) by 1, leaving the quantity $F - E + V$ unchanged. Repeat until all faces are triangles.

    3. **Removing Triangular Faces (Edges/Vertices Step):**
       * **Case A:** Remove an outer edge and an outer face that has an edge on the boundary. This removes 1 face and 1 edge, leaving $F - E + V$ unchanged.
       * **Case B:** Remove an outer face that has two edges on the boundary and one new vertex ($V$) created. This removes 1 face, 2 edges, and 1 vertex, leaving $F - E + V$ unchanged.

    4. **Final Step:** Continue this process until only a single triangle remains. For a single triangle:
       $$F = 1$$ (the region inside the triangle)
       $$E = 3$$ (the three sides)
       $$V = 3$$ (the three corners)
       $$F - E + V = 1 - 3 + 3 = 1$$

    Wait! The formula is for 3D shapes, and we removed one face (Step 1). The planar graph has $F_{graph} - E_{graph} + V_{graph} = 1$.
    Since the original 3D polyhedron has one more face (the removed one):
    $$F_{polyhedron} = F_{graph} + 1$$
    $$F_{polyhedron} - E_{polyhedron} + V_{polyhedron} = (F_{graph} + 1) - E_{graph} + V_{graph} = (F_{graph} - E_{graph} + V_{graph}) + 1 = 1 + 1 = 2$$
    Thus, $F - E + V = 2$. 
    """)
    return generate_explanation(title, topic, derivation)

def explain_complex_formula():
    """Explains the algebraic manipulation for the complex formula."""
    title = "Algebraic Relationship: $A = D + (A \\cdot D \\cdot 2^{D}/18)$"
    topic = (
        "This is a general algebraic equation establishing a relationship between the variables $A$ and $D$. "
        "Since it is not a universally recognized physical or mathematical constant, the primary goal is "
        "to isolate one variable in terms of the other (in this case, solving for $A$ in terms of $D$). "
        "This requires standard algebraic manipulation, including isolating terms involving $A$ and factoring."
    )
    derivation = textwrap.dedent("""
    Goal: Solve for $A$ in terms of $D$.

    Starting Equation:
    $$A = D + A \\left( \\frac{D \\cdot 2^{D}}{18} \\right)$$

    1. **Move all terms containing $A$ to the Left Hand Side (LHS):**
       $$A - A \\left( \\frac{D \\cdot 2^{D}}{18} \\right) = D$$

    2. **Factor out $A$ from the LHS:**
       $$A \\left( 1 - \\frac{D \\cdot 2^{D}}{18} \\right) = D$$

    3. **Simplify the term inside the parenthesis by finding a common denominator (18):**
       $$A \\left( \\frac{18}{18} - \\frac{D \\cdot 2^{D}}{18} \\right) = D$$
       $$A \\left( \\frac{18 - D \\cdot 2^{D}}{18} \\right) = D$$

    4. **Isolate $A$ by multiplying both sides by the reciprocal of the term in parentheses:**
       $$A = D \\left( \\frac{18}{18 - D \\cdot 2^{D}} \\right)$$

    Final derived expression for $A$:
    $$A = \\frac{18D}{18 - D \\cdot 2^{D}}$$
    """)
    return generate_explanation(title, topic, derivation)


if __name__ == "__main__":
    print("--- BEGINNING SCIENCE AND MATH EXPLANATION LOG ---")
    print(explain_phi())
    print(explain_emc2())
    print(explain_euler_polyhedron())
    print(explain_complex_formula())
    print("--- END SCIENCE AND MATH EXPLANATION LOG ---")

# Note: The output uses LaTeX format for mathematical expressions, which renders correctly
# in environments that support it (e.g., Markdown viewers).

